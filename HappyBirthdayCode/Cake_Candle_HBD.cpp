#include <stdio.h>
#ifndef REPS
#define REPS 64
#endif
#ifndef DELAY
#define DELAY 99999999UL
#endif
#ifdef __unix__
#define CLR "\33[H\33[2J"
#else
#define CLR "\f"
#endif
#define R9(x)R8(x)x
#define R8(x)R7(x)x
#define R7(x)R6(x)x
#define R6(x)R5(x)x
#define R5(x)R4(x)x
#define R4(x)R3(x)x
#define R3(x)R2(x)x
#define R2(x)x x
#define CP1(from, to, i)V((to)[i]=(from)[i])
#define CP3(from, to)do {int z=0;R3((to)[z]=(from)[z];++z;)} while(0)
#define V(x)((void)(x))
static const char LET_THEM_EAT[] =
    R2("\16$   \1")"\16$'_'\1\16.|.\1\16|@|\1\2.\177\13-|@|\177\13-.\1"
    "./\13:|@|:\13\\.\1|\4HAPPY\4\"^\"\2BIRTHDAY!\2|\1|\\\33/|\1"
    "| '\177\31-' |\1|x "R4("%\5")"% x|\1| x"R8(" %%")" x |\1"
    "|"R4("\5%")"\5|\1|+\33+|\1|"R9("\2#")"\2|\1 \\\33/\1\2'\177\31-'\1",
AGNI[] = ")\\ )\\\\ )\\ /)//)/) ",
TAIL[] = R3(R2("\\   ")"\\  : "R3(" /")"  :  ")R4(" *")R9(" ")" ";
volatile char foo;
static void render(char *const *, char *, const char *, unsigned);
static void hold(void);
int main(void) {
    static char image[16384];
    char *imgref[3], **iq=imgref;
    char *q=image, c, d;
    const char *p=LET_THEM_EAT;
    unsigned long rep=REPS;
    while(!!(c=*(p++))) {
#   define qup(x)V(*(q++)=(x))
        if(c == 1) qup('\n');
        else if(c == '$') *(iq++)=q;
        else if(c == 127)
            for(c = *(p++), d = *(p++); c--;) qup(d);
        else if(c < ' ')
            while(c--) qup(' ');
        else qup(c);
#   undef qup
    }
    for(*q='\0', p=AGNI; rep; V(*(p+=3)||((p=AGNI), rep--)), hold())
        render(imgref, image, p, 2);
    CP3("   ", imgref[2]);
    for(p=TAIL; *p; p+=3, hold())
        render(imgref, image, p, 3);
    return 0;
}
static void render(char *const *ir, char *i, const char *f, unsigned n) {
    unsigned m;
    for(m=0, --n; m < n; m++) CP3(ir[m+1], ir[m]);
    CP3(f, ir[n]);
    printf(CLR"%s", i);
    fflush(stdout);
}
static void hold(void) {
    unsigned long delay=DELAY;
    while(delay--) if(!foo) foo=0;
}