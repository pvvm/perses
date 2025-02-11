



import static com.sun.tools.classfile.TypeAnnotation.TargetType.*;

public class Constructors {

    @TADescriptions({
        @TADescription(annotation = "TA", type = METHOD_RETURN),
        @TADescription(annotation = "TB", type = METHOD_RETURN),
        @TADescription(annotation = "TC", type = METHOD_FORMAL_PARAMETER, paramIndex = 0)
    })
    public String regularClass() {
        return "class Test { @TA Test() {}" +
                           " @TB Test(@TC int b) {} }";
    }

    @TADescriptions({
        @TADescription(annotation = "TA", type = METHOD_RETURN, genericLocation = {1, 0}),
        @TADescription(annotation = "TB", type = METHOD_RETURN, genericLocation = {1, 0}),
        @TADescription(annotation = "TC", type = METHOD_FORMAL_PARAMETER, paramIndex = 0)
    })
    @TestClass("Test$Inner")
    public String innerClass() {
        return "class Test { class Inner {" +
               " @TA Inner() {}" +
               " @TB Inner(@TC int b) {}" +
               " } }";
    }

    @TADescriptions({
        @TADescription(annotation = "TA", type = METHOD_RECEIVER),
        @TADescription(annotation = "TB", type = METHOD_RETURN, genericLocation = {1, 0}),
        @TADescription(annotation = "TC", type = METHOD_RECEIVER),
        @TADescription(annotation = "TD", type = METHOD_RETURN, genericLocation = {1, 0}),
        @TADescription(annotation = "TE", type = METHOD_FORMAL_PARAMETER, paramIndex = 0)
    })
    @TestClass("Test$Inner")
    public String innerClass2() {
        return "class Test { class Inner {" +
               " @TB Inner(@TA Test Test.this) {}" +
               " @TD Inner(@TC Test Test.this, @TE int b) {}" +
               " } }";
    }

    @TADescriptions({
        @TADescription(annotation = "TA", type = METHOD_RECEIVER),
        @TADescription(annotation = "TB", type = METHOD_RECEIVER, genericLocation = {1, 0}),
        @TADescription(annotation = "TC", type = METHOD_RETURN, genericLocation = {1, 0, 1, 0}),
        @TADescription(annotation = "TD", type = METHOD_RECEIVER, genericLocation = {1, 0}),
        @TADescription(annotation = "TE", type = METHOD_RETURN, genericLocation = {1, 0, 1, 0}),
        @TADescription(annotation = "TF", type = METHOD_FORMAL_PARAMETER, paramIndex = 0)
    })
    @TestClass("Outer$Middle$Inner")
    public String innerClass3() {
        return "class Outer { class Middle { class Inner {" +
               " @TC Inner(@TA Outer. @TB Middle Middle.this) {}" +
               " @TE Inner(@TD Middle Outer.Middle.this, @TF int b) {}" +
               " } } }";
    }

    @TADescriptions({
        @TADescription(annotation = "TA", type = CONSTRUCTOR_INVOCATION_TYPE_ARGUMENT,
                typeIndex = 0, offset = 4),
        @TADescription(annotation = "TB", type = CONSTRUCTOR_INVOCATION_TYPE_ARGUMENT,
                typeIndex = 0, offset = 0)
    })
    public String generic1() {
        return "class Test { <T> Test(int i) { new <@TA T>Test(); }" +
                           " <T> Test() { <@TB String>this(0); } }";
    }

    @TADescriptions({
        @TADescription(annotation = "TA", type = CONSTRUCTOR_INVOCATION_TYPE_ARGUMENT,
                typeIndex = 0, offset = 0)
    })
    public String generic2() {
        return "class Super { <T> Super(int i) { } } " +
                "class Test extends Super { <T> Test() { <@TA String>super(0); } }";
    }

}
