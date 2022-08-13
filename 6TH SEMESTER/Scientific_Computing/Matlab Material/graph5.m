% Illustration of meshgrid
x=-1:0.05:1;
y=x;
[xi yi]=meshgrid(x,y);
zi=yi.^2-xi.^2;
mesh(xi,yi,zi)
axis off
% To plot the graph of the mesh surface along with contour plot beneath the
% plotted surface:
meshc(xi,yi,zi)