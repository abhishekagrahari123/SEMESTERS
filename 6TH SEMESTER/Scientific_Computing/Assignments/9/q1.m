clc;
clear;

L = 0.5;
T = 1;
h = 0.1;
r = 0.25;
k = 0.0025;
Nx = 5;
Nt = 400;
u = zeros(Nx+1, Nt+1);
err = zeros(Nx+1, Nt+1);
pos = zeros(1,Nx+1);
time = zeros(1,Nt+1);
for n = 1:Nx+1
    u(n,1) = 0;
    pos(n) = (n-1)*h;
end
for n = 1:Nt+1
    time(n) = (n-1)*k;
end
MMl = zeros(Nx+1, Nx+1);
for i = 1:Nx+1
    MMl(i,i) = 1;
end

aar = zeros(1,Nx);
bbr = zeros(1,Nx+1);
ccr = zeros(1,Nx);
aar(1:Nx-1) = r;
aar(Nx) = 2*r;
bbr(1:Nx+1) = 1.-2.*r;
ccr(2:Nx) = r;
ccr(1) = 2*r;
MMr = diag(bbr, 0) + diag(aar, -1) + diag(ccr, 1);

Cr = zeros(1,Nx+1);
Cr(Nx+1) = 2*h*r;
for j = 2:Nt+1
    u(1:Nx+1,j) = MMl\MMr*u(1:Nx+1,j-1) + MMl\transpose(Cr);
end

for j = 1:Nt+1
    for i = 1:Nx+1
        err(i, j) = abs(act(i,j,h,k)-u(i,j));
    end
end

figure(1);
surf(time,pos,u);
shading interp;
xlabel('Time');
ylabel('Position');
title('Explicit Scheme: U(x,t)');

figure(2);
surf(time, pos, err);
shading interp;
xlabel('Time');
ylabel('Position');
title('Explicit Scheme: Error value');

fprintf('Time \t     x=0 \t   x=0.1 \t   x=0.2 \t  x=0.3 \t  x=0.4 \t  x=0.5\n')
for t = 1:Nt+1
    actt = (t-1)*k;
    if actt == 0.01 || actt == 0.05 || actt == 0.5 || actt == 1
            fprintf('%.2f \t %10f \t %5f \t %5f \t %5f \t %5f \t %5f \n',actt, u(1,t), u(2,t),u(3,t), u(4,t), u(5,t), u(6,t));
    end
end

function val = act(i,j,h,k)
    t = (j-1)*k;
    x = (i-1)*h;
    val = 2*t;
    val = val + 1/2*((12*x*x-1)/6);
    sum = 0;
    TOL = 10^(-10);
    n = 1;
    while abs(term(x,t,n)) > TOL
        sum = sum + term(x,t,n);
        n = n + 1;
    end
    val = val - sum;
end

function val = term(x,t,n)
    val = ((-1)^n*exp(-4*pi*pi*n*n*t)*cos(2*n*pi*x))/n^2;
    val = val/(pi*pi);
end
