clc;
clear;

L = 1;
t = 0.1;
h = 0.1;
k = 0.01;
Nt = round(t/k);
Nx = round(L/h);
r = k/(h^2);
x = linspace(0,1,Nx+1);
t = linspace(0,0.1,Nt+1);
u = zeros(Nx+1, Nt+1);
for n = 1:Nx+1
    if x(n) <= 0.5
        u(n,1) = 2*x(n);
    else
        u(n,1) = 2*(1-x(n));
    end
end

for j = 1:Nt+1
    u(1,j) = 0;
    u(Nx+1,j) = 0;
end

aal(1:Nx-2) = -r;
bbl(1:Nx-1) = 2.+2.*r;
ccl(1:Nx-2) = -r;
MMl = diag(bbl,0) + diag(aal,-1) + diag(ccl,1);
aar(1:Nx-2)=r;
bbr(1:Nx-1) = 2.-2.*r;
ccr(1:Nx-2) = r;
MMr = diag(bbr, 0) + diag(aar, -1) + diag(ccr, 1);

for j = 2:Nt+1
    cons = zeros(Nx-1, 1);
    cons(1, 1) = r*u(1, j-1) + r*u(1,j);
    cons(Nx-1, 1) = r*u(Nx+1, j-1) + r*u(Nx+1, j);
    u(2:Nx,j) = MMl\MMr*u(2:Nx,j-1) + MMl\cons;
end

surf(t,x,u)
title('Solution by Crank-Nicholson method');
xlabel('x');
ylabel('t');