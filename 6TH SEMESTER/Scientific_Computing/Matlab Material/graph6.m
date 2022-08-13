

% Script file graph6.

% Surface plot of the hyperbolic paraboloid z = y^2 - x^2
% and its level curves.

x = -1:.05:1;
y = x;
[xi,yi] = meshgrid(x,y);
zi = yi.^2 - xi.^2;
%mesh(xi,yi,zi)
meshc(xi,yi,zi)
hold on
surfc(xi,yi,zi)
%plots surfaces with level lines beneath.surf plots surface without level
%curves.
colormap copper
% to paint the surface using user supplied colors.
shading interp
% option for shading after interpolation
view([25,15,20])
% for setting the view angle 
grid off
title('Figure C')
h = get(gca,'Title');
set(h,'FontSize',12)
xlabel('x')
h = get(gca,'xlabel');
set(h,'FontSize',12)
ylabel('y')
h = get(gca,'ylabel');
set(h,'FontSize',12)
zlabel('z')
h = get(gca,'zlabel');
set(h,'FontSize',12)
pause(5)
figure
%prompts MATLAB to create a new figure
contourf(zi), hold on, shading flat
%hold on - to hold the current plot and all axis properties so that the
%subsequent graphing commands add to the existing graph.
[c,h] = contour(zi,'k-'); clabel(c,h)
title('The level curves of z = y^2 - x^2.')
h = get(gca,'Title');
set(h,'FontSize',12)
xlabel('x')
h = get(gca,'xlabel');
set(h,'FontSize',12)
ylabel('y')
h = get(gca,'ylabel');
set(h,'FontSize',12)

