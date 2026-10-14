public class BootCamp extends ProgramaAcademico {

    public BootCamp() {
        super("BootCamp");
    }

    @Override
    public boolean estudianteAprobado(Alumno alumno) {
        if (alumno.getNotas().size() != 3) {
            return false;
        }

        for (double nota : alumno.getNotas()) {
            if (nota < 14) {
                return false;
            }
        }

        return true;
    }
}