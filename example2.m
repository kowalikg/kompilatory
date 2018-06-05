A = [1,1;7,1];
B = [2,1;1,1];
C = [1;7];
D = [0,0;0,0];
print "A", A;
print "B", B;
print "C", C;
print "D", D;
print "A*B", A*B;
print "A.*B", A.*B;
print "A/B", A/B;
print "A./B", A./B;
A *= B;
print "A*=B", A;
print "A.*B", A.*B;
print "-A", -A;
print "A'", A';
print "A*C", A*C;
print "A/D", A/D;

D[0,0] = 3;
D[0,1] += 1;
print "D", D;

x = 0;
y = -7;
print "x + y", x + y;
print "y", -y;
x += y;
print "x+=y", x;

if (y > 5)
print "y>5";
else
print "y<=5";

N = 3;
M = 4;

for j = 0: M {
    for i = 0:N {
        if (i > 1){
            print "Kuniec";
            break;
        }
        if (i > 0){
            print "Prawie kuniec";
            continue;
        }
        print i;
    }
    if (j > 2){
        print "Koniec wszystkiego";
        break;
    }

}
k = 1;
while(k>0) {
    i = 0;
    if(k<5)
        i = 1;
    else if(k<10)
        i = 2;
    else
        i = 3;
    break;
       print i;
}
