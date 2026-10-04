public abstract class ProgramaAcademico {
    protected String nombre;

    public ProgramaAcademico(String nombre) {
        this.nombre = nombre;
    }

    public String getNombre() {
        return nombre;
    }

    public abstract boolean estudianteAprobado(Alumno alumno);
}
