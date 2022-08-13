clc;
clear;
TOL = 10^(-3);

f1 = @(x1,x2) sin(x1*x2) + x1-x2;
f2 = @(x1,x2) x2*cos(x1*x2) + 1;
df1_dx1 = @(x1,x2) x2*cos(x1*x2) + 1;
df1_dx2 = @(x1,x2) x1*cos(x1*x2)-1;
df2_dx1 = @(x1,x2) -x2*x2*sin(x1*x2);
df2_dx2 = @(x1,x2) cos(x1*x2) - x1*x2*sin(x1*x2);
J = @(x1,x2) [df1_dx1(x1,x2) df1_dx2(x1,x2); df2_dx1(x1,x2) df2_dx2(x1,x2)];
h = @(x1,x2) -inv(J(x1,x2))*[f1(x1,x2); f2(x1,x2)];

i = 1;
h1 = zeros(100);
h2 = zeros(100);
X1 = zeros(100);
X2 = zeros(100);
X1(i) = 1;
X2(i) = 2;
H = h(X1(i),X2(i));
h1(i) = H(1,1);
h2(i) = H(2,1);
fprintf("Iteration        x1           x2          f1(x1,x2)       f2(x1,x2)\n");
while abs(h1(i)) + abs(h2(i)) >= TOL
    fprintf(" %5d %14.8f %14.8f %14.8f %14.8f\n",i,X1(i),X2(i),f1(X1(i),X2(i)),f2(X1(i),X2(i)));
    i = i + 1;
    X1(i) = X1(i-1) + h1(i-1);
    X2(i) = X2(i-1) + h2(i-1);
    H = h(X1(i),X2(i));
    h1(i) = H(1,1);
    h2(i) = H(2,1);
end
fprintf(" %5d %14.8f %14.8f %14.8f %14.8f\n",i,X1(i),X2(i),f1(X1(i),X2(i)),f2(X1(i),X2(i)));

