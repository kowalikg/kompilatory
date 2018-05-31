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

y = 4 + 0;
print y, 14;
M = [1,2;5,6];
print M;
M[0,0] = 5;
print M;
M[0,0] -= 5;
print M;

if (y > 5)
print y;
else
print "olo";

print -M;
print M';
N = [8,9;1,4];
A = M/N;
print A./N;