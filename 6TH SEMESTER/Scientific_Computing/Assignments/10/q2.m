clc;
clear;

h = 0.1;
k = 0.1;
r = k/(h*h);
Nx = round(1/h);
Nt = round(1/k);
u = zeros(Nx+1, Nx+1, Nt+1);
mid = zeros(Nx+1, Nx+1, Nt);

for i = 1:Nx+1
    for j = 1:Nx+1
        x = (i-1)*h;
        y = (j-1)*h;
        u(i,j,1) = sin(pi*x)*sin(pi*y);
    end
end
x = 0:h:1;
y = 0:h:1;
aal = zeros(1,Nx-2);
bbl = zeros(1,Nx-1);
ccl = zeros(1,Nx-2);
aal(1:Nx-2) = -r;
bbl(1:Nx-1) = 2.+2.*r;
ccl(1:Nx-2) = -r;
MMl = diag(bbl,0) + diag(aal,-1) + diag(ccl,1);
for t = 2:Nt+1  
    for j = 2:Nx
        MMr1 = zeros(1,Nx-1);
        for i = 2:Nx
            MMr1(i-1) = r*u(i,j-1,t-1) + (2-2*r)*u(i,j,t-1) + r*u(i,j+1,t-1);
        end
        mid(2:Nx,j,t-1) = MMl\transpose(MMr1);    
    end
    for i = 2:Nx
        MMr2 = zeros(1,Nx-1);
        for j = 2:Nx
            MMr2(j-1) = r*mid(i+1,j,t-1) + (2-2*r)*mid(i,j,t-1) + r*mid(i-1,j,t-1);
        end
        u(i,2:Nx,t) = MMl\transpose(MMr2);
    end
end

for time = 0:0.2:1
    figure();
    idx = round(time/k);
    surf(x,y,u(:,:,idx+1));
    xlabel('x-axis');
    ylabel('y-axis');
    title(sprintf('Plot of U(x,y,%.1f) ADI Scheme', time));
end
