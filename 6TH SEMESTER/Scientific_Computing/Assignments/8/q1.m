clc;
clear;
h = 0.05; 
% h = 0.01;
k = 0.01;
Nx = round(1/h);
Ny = round(0.1/k);
u = zeros(Ny+1, Nx+1);
err = zeros(Ny+1, Nx+1);
actual = zeros(Ny+1, Nx+1);
r = k/(h^2)

% boundary conditions
for j = 1:Ny+1
    u(j,1) = 0;
    u(j, Nx+1) = 0;
end

% initial condition
for i = 1:Nx+1
    xi = 0+(i-1)*h;
    u(1, i) = sin(pi*xi);
end

% u(i, j) for all valid i, j
for j = 2:Ny
    for i = 2:Nx
        u(j, i) = r*u(j-1, i-1) + (1-2*r)*u(j-1,i) + r*u(j-1, i+1);
    end
end
for j = 1:Ny+1
    for i = 1:Nx+1
        err(j, i) = abs(act(j,i,h,k)-u(j,i));
    end
end
for j = 1:Ny+1
    for i = 1:Nx+1
        actual(j, i) = act(j,i,h,k);
    end
end
x = linspace(0,1,Nx+1);
t = linspace(0,0.1, Ny+1);
[xm ,tm] = meshgrid(x,t);

figure;
surf(x, t, u);
figure;
surf(xm, tm, u);
% figure(2);
% surf(xm, tm, err);
% 
% figure(3);
% surf(xm, tm,actual); 

function val = act(j,i,h,k)
    t = (j-1)*k;
    x = (i-1)*h;
    val = exp(-(pi^2)*t)*sin(pi*x);
end




