#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <stack>
#include <queue>
#include <iomanip>
#include <algorithm>
#include <limits>

using namespace std;

const string ARCHIVO_ALUMNOS = "alumnos.txt";
const string ARCHIVO_PROFESORES = "profesores.txt";
const string ARCHIVO_CERTIFICADOS = "certificados_pendientes.txt";

// ==================== JERARQUIA DE PERSONAS ====================

class Persona {
protected:
    string cedula;
    string nombre;
    string correo;

public:
    Persona(const string& c, const string& n, const string& e)
        : cedula(c), nombre(n), correo(e) {}

    virtual ~Persona() = default;

    string getCedula() const { return cedula; }
    string getNombre() const { return nombre; }
    string getCorreo() const { return correo; }
};

// ==================== POLIMORFISMO DE PROGRAMAS ====================

class ProgramaAcademico {
public:
    virtual ~ProgramaAcademico() = default;

    virtual bool evaluarAprobacion(const vector<double>& notas) const = 0;
    virtual string getNombre() const = 0;
};

class Curso : public ProgramaAcademico {
private:
    double calcularPromedio(const vector<double>& notas) const {
        double suma = 0;
        for (double nota : notas) suma += nota;
        return suma / notas.size();
    }

public:
    bool evaluarAprobacion(const vector<double>& notas) const override {
        return notas.size() == 3 && calcularPromedio(notas) >= 10.0;
    }

    string getNombre() const override {
        return "Curso";
    }
};

class Diplomado : public ProgramaAcademico {
private:
    double calcularPromedio(const vector<double>& notas) const {
        double suma = 0;
        for (double nota : notas) suma += nota;
        return suma / notas.size();
    }

public:
    bool evaluarAprobacion(const vector<double>& notas) const override {
        return notas.size() == 3 && calcularPromedio(notas) >= 14.0;
    }

    string getNombre() const override {
        return "Diplomado";
    }
};

class Bootcamp : public ProgramaAcademico {
public:
    bool evaluarAprobacion(const vector<double>& notas) const override {
        if (notas.size() != 3) return false;

        for (double nota : notas) {
            if (nota < 14.0) return false;
        }

        return true;
    }

    string getNombre() const override {
        return "Bootcamp";
    }
};

ProgramaAcademico* crearPrograma(const string& tipo) {
    if (tipo == "Curso") return new Curso();
    if (tipo == "Diplomado") return new Diplomado();
    if (tipo == "Bootcamp") return new Bootcamp();

    return nullptr;
}

// ==================== ALUMNO ====================

class Alumno : public Persona {
private:
    vector<double> notas;
    ProgramaAcademico* programa;

public:
    Alumno(const string& c, const string& n, const string& e,
           ProgramaAcademico* p)
        : Persona(c, n, e), programa(p) {}

    ~Alumno() override {
        delete programa;
    }

    bool agregarNota(double nota) {
        if (notas.size() >= 3) return false;

        notas.push_back(nota);
        return true;
    }

    bool eliminarUltimaNota() {
        if (notas.empty()) return false;

        notas.pop_back();
        return true;
    }

    const vector<double>& getNotas() const {
        return notas;
    }

    string getPrograma() const {
        return programa->getNombre();
    }

    bool estaAprobado() const {
        return programa->evaluarAprobacion(notas);
    }

    double promedio() const {
        if (notas.empty()) return 0.0;

        double suma = 0;
        for (double nota : notas) suma += nota;

        return suma / notas.size();
    }
};

// ==================== PROFESOR ====================

class Profesor : public Persona {
private:
    string especialidad;
    string materia;

public:
    Profesor(const string& c, const string& n, const string& e,
             const string& esp, const string& mat)
        : Persona(c, n, e), especialidad(esp), materia(mat) {}

    string getEspecialidad() const {
        return especialidad;
    }

    string getMateria() const {
        return materia;
    }
};

// Registro usado por la Pila LIFO para Deshacer
struct RegistroNota {
    Alumno* alumno;
    double nota;
};

// ==================== SISTEMA PRINCIPAL ====================

class SistemaSGA {
private:
    vector<Alumno*> alumnos;
    vector<Profesor*> profesores;

    // Pila LIFO: guarda las ultimas notas introducidas
    stack<RegistroNota> pilaDeshacer;

    Alumno* buscarAlumno(const string& cedula) const {
        for (Alumno* alumno : alumnos) {
            if (alumno->getCedula() == cedula) {
                return alumno;
            }
        }

        return nullptr;
    }

    vector<string> dividir(const string& linea) const {
        vector<string> partes;
        string parte;
        stringstream ss(linea);

        while (getline(ss, parte, ',')) {
            partes.push_back(parte);
        }

        return partes;
    }

    void escribirNotas(ofstream& archivo,
                       const vector<double>& notas) const {
        for (int i = 0; i < 3; ++i) {
            if (i > 0) archivo << ",";

            if (i < static_cast<int>(notas.size())) {
                archivo << notas[i];
            } else {
                archivo << "0";
            }
        }
    }

public:
    ~SistemaSGA() {
        // Liberacion manual de memoria solicitada por el proyecto
        for (Alumno* alumno : alumnos) {
            delete alumno;
        }

        for (Profesor* profesor : profesores) {
            delete profesor;
        }

        alumnos.clear();
        profesores.clear();
    }

    // ==================== PERSISTENCIA ====================

    void cargarArchivos() {
        ifstream archivoAlumnos(ARCHIVO_ALUMNOS);
        string linea;

        while (getline(archivoAlumnos, linea)) {
            if (linea.empty()) continue;

            vector<string> datos = dividir(linea);

            if (datos.size() < 7) continue;

            ProgramaAcademico* programa = crearPrograma(datos[3]);

            if (programa == nullptr) continue;

            Alumno* alumno = new Alumno(
                datos[0], datos[1], datos[2], programa
            );

            for (int i = 4; i < 7; ++i) {
                try {
                    double nota = stod(datos[i]);

                    // En el formato del proyecto, 0 representa ausencia de nota.
                    if (nota != 0) {
                        alumno->agregarNota(nota);
                    }
                } catch (...) {
                    // Ignorar una nota mal formada sin detener el sistema.
                }
            }

            alumnos.push_back(alumno);
        }

        archivoAlumnos.close();

        ifstream archivoProfesores(ARCHIVO_PROFESORES);

        while (getline(archivoProfesores, linea)) {
            if (linea.empty()) continue;

            vector<string> datos = dividir(linea);

            if (datos.size() < 5) continue;

            profesores.push_back(new Profesor(
                datos[0], datos[1], datos[2],
                datos[3], datos[4]
            ));
        }

        archivoProfesores.close();
    }

    void guardarAlumnos() const {
        ofstream archivo(ARCHIVO_ALUMNOS, ios::trunc);

        for (const Alumno* alumno : alumnos) {
            archivo << alumno->getCedula() << ","
                    << alumno->getNombre() << ","
                    << alumno->getCorreo() << ","
                    << alumno->getPrograma() << ",";

            escribirNotas(archivo, alumno->getNotas());

            archivo << "\n";
        }
    }

    void guardarProfesores() const {
        ofstream archivo(ARCHIVO_PROFESORES, ios::trunc);

        for (const Profesor* profesor : profesores) {
            archivo << profesor->getCedula() << ","
                    << profesor->getNombre() << ","
                    << profesor->getCorreo() << ","
                    << profesor->getEspecialidad() << ","
                    << profesor->getMateria() << "\n";
        }
    }

    // ==================== OPCION 1 ====================

    void registrarAlumno() {
        string cedula, nombre, correo, tipo;

        cout << "\n--- REGISTRAR ALUMNO ---\n";

        cout << "Cedula/ID: ";
        getline(cin, cedula);

        if (buscarAlumno(cedula) != nullptr) {
            cout << "Error: ya existe un alumno con esa cedula.\n";
            return;
        }

        cout << "Nombre completo: ";
        getline(cin, nombre);

        cout << "Correo: ";
        getline(cin, correo);

        cout << "Programa (Curso/Diplomado/Bootcamp): ";
        getline(cin, tipo);

        ProgramaAcademico* programa = crearPrograma(tipo);

        if (programa == nullptr) {
            cout << "Error: programa no valido.\n";
            return;
        }

        // Memoria dinamica mediante new
        alumnos.push_back(
            new Alumno(cedula, nombre, correo, programa)
        );

        // Persistencia inmediata
        guardarAlumnos();

        cout << "Alumno registrado correctamente.\n";
    }

    // ==================== OPCION 2 ====================

    void registrarProfesor() {
        string cedula, nombre, correo, especialidad, materia;

        cout << "\n--- REGISTRAR PROFESOR ---\n";

        cout << "Cedula/ID: ";
        getline(cin, cedula);

        cout << "Nombre completo: ";
        getline(cin, nombre);

        cout << "Correo: ";
        getline(cin, correo);

        cout << "Especialidad: ";
        getline(cin, especialidad);

        cout << "Materia: ";
        getline(cin, materia);

        profesores.push_back(
            new Profesor(
                cedula, nombre, correo,
                especialidad, materia
            )
        );

        guardarProfesores();

        cout << "Profesor registrado correctamente.\n";
    }

    // ==================== OPCION 3 ====================

    void registrarNota() {
        string cedula;

        cout << "\n--- REGISTRAR NOTA ---\n";

        cout << "Cedula del alumno: ";
        getline(cin, cedula);

        Alumno* alumno = buscarAlumno(cedula);

        if (alumno == nullptr) {
            cout << "Error: alumno no encontrado.\n";
            return;
        }

        if (alumno->getNotas().size() >= 3) {
            cout << "Error: el alumno ya tiene 3 notas.\n";
            return;
        }

        double nota;

        cout << "Ingrese la nota: ";

        if (!(cin >> nota)) {
            cout << "Error: Ingrese un valor numerico valido.\n";

            cin.clear();
            cin.ignore(
                numeric_limits<streamsize>::max(),
                '\n'
            );

            return;
        }

        cin.ignore(
            numeric_limits<streamsize>::max(),
            '\n'
        );

        alumno->agregarNota(nota);

        // Se guarda el alumno en la pila.
        // Asi Deshacer no necesita volver a pedir la cedula.
        pilaDeshacer.push({alumno, nota});

        // Persistencia inmediata
        guardarAlumnos();

        cout << "Nota registrada correctamente.\n";
    }

    // ==================== OPCION 4 ====================

    void deshacerNota() {
        cout << "\n--- DESHACER ULTIMO REGISTRO DE NOTA ---\n";

        if (pilaDeshacer.empty()) {
            cout << "No hay notas para deshacer en esta sesion.\n";
            return;
        }

        // LIFO: se recupera la ultima nota introducida
        RegistroNota registro = pilaDeshacer.top();
        pilaDeshacer.pop();

        if (registro.alumno->eliminarUltimaNota()) {
            guardarAlumnos();

            cout << "Deshacer realizado correctamente.\n";
            cout << "La ultima nota ingresada fue eliminada.\n";
        }
    }

    // ==================== OPCION 5 ====================

    void generarCertificados() const {
    // Cola FIFO
    queue<Alumno*> colaCertificados;

    for (Alumno* alumno : alumnos) {
        if (alumno->estaAprobado()) {
            colaCertificados.push(alumno);
        }
    }

    ofstream archivo(
        ARCHIVO_CERTIFICADOS,
        ios::trunc
    );

    archivo << "CERTIFICADOS PENDIENTES\n";
    archivo << "Total de graduandos en cola: "
            << colaCertificados.size() << "\n\n";

    int posicion = 1;

    while (!colaCertificados.empty()) {
        Alumno* alumno = colaCertificados.front();
        colaCertificados.pop();

        archivo << posicion << ". ["
                << alumno->getCedula() << "] "
                << alumno->getNombre() << "\n";

        ++posicion;
    }

    archivo.close();

    cout << "Cola generada correctamente en "
         << ARCHIVO_CERTIFICADOS << ".\n";
}

    // ==================== OPCION 6 ====================

    void reporteGeneral() const {
        cout << "\n================ REPORTE GENERAL ================\n";

        cout << "\nALUMNOS:\n";

        for (const Alumno* alumno : alumnos) {
            cout << "["
                 << alumno->getCedula()
                 << "] "
                 << alumno->getNombre()
                 << " | Programa: "
                 << alumno->getPrograma()
                 << " | Notas: ";

            for (double nota : alumno->getNotas()) {
                cout << nota << " ";
            }

            cout << "| Promedio: "
                 << fixed << setprecision(1)
                 << alumno->promedio();

            cout << " | Estatus: "
                 << (alumno->estaAprobado()
                     ? "APROBADO"
                     : "REPROBADO")
                 << "\n";
        }

        cout << "\nPROFESORES:\n";

        for (const Profesor* profesor : profesores) {
            cout << "["
                 << profesor->getCedula()
                 << "] "
                 << profesor->getNombre()
                 << " | Especialidad: "
                 << profesor->getEspecialidad()
                 << " | Materia: "
                 << profesor->getMateria()
                 << "\n";
        }

        cout << "==================================================\n";
    }
};

// ==================== VALIDACION DEL MENU ====================

int leerOpcion() {
    int opcion;

    cout << "\nSeleccione una opcion (1-7): ";

    if (!(cin >> opcion)) {
        cout << "Error: Ingrese un valor numerico valido.\n";

        cin.clear();
        cin.ignore(
            numeric_limits<streamsize>::max(),
            '\n'
        );

        return -1;
    }

    cin.ignore(
        numeric_limits<streamsize>::max(),
        '\n'
    );

    return opcion;
}

// ==================== MAIN ====================

int main() {
    SistemaSGA sistema;

    // Carga los datos persistidos al iniciar.
    sistema.cargarArchivos();

    int opcion;

    do {
        cout << "\n==================================================\n";
        cout << "SGA-DO: SISTEMA DIPLOMADOSONLINE\n";
        cout << "==================================================\n";
        cout << "1. Registrar Alumno\n";
        cout << "2. Registrar Profesor\n";
        cout << "3. Registrar Notas a un Alumno\n";
        cout << "4. Deshacer Ultimo Registro de Nota\n";
        cout << "5. Generar Cola de Certificados\n";
        cout << "6. Mostrar Reporte General\n";
        cout << "7. Salir\n";
        cout << "==================================================\n";

        opcion = leerOpcion();

        switch (opcion) {
            case 1:
                sistema.registrarAlumno();
                break;

            case 2:
                sistema.registrarProfesor();
                break;

            case 3:
                sistema.registrarNota();
                break;

            case 4:
                sistema.deshacerNota();
                break;

            case 5:
                sistema.generarCertificados();
                break;

            case 6:
                sistema.reporteGeneral();
                break;

            case 7:
                cout << "Cerrando SGA-DO...\n";
                break;

            case -1:
                break;

            default:
                cout << "Opcion no valida. Intente nuevamente.\n";
        }

    } while (opcion != 7);

    return 0;
}
