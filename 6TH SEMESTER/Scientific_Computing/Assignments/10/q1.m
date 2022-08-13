clc;
clear;

h = 0.1;
r = 1/4;
k = r*h*h;
Nx = round(1/h);
Nt = round(1/k);
u = zeros(Nx+1, Nx+1, Nt+1);

for i = 1:Nx+1
    for j = 1:Nx+1
        x = (i-1)*h;
        y = (j-1)*h;
        u(i,j,1) = sin(pi*x)*sin(pi*y);
    end
end

x = 0:h:1;
y = 0:h:1;

for t = 2:Nt+1
    for i = 2:Nx
        for j = 2:Nx
            u(i,j,t) = r*u(i+1,j,t-1) + r*u(i-1,j,t-1) + (1-4*r)*u(i,j,t-1)+r*u(i,j+1,t-1)+r*u(i,j-1,t-1);
        end
    end
end
 
for time = 0:0.2:1
    figure();
    idx = round(time/k);
    surf(x,y,u(:,:,idx+1));
    xlabel('x-axis');
    ylabel('y-axis');
    title(sprintf('Plot of U(x,y,%.1f): Explicit Scheme', time));
end
