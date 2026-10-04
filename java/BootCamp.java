public class BootCamp extends ProgramaAcademico {

    public BootCamp() {
        super("BootCamp");
    }

    @Override
    public boolean estudianteAprobado(Alumno alumno) {
        if (alumno.getNotas().isEmpty()) {
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