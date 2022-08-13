
% Script file graph3.
% Graphs of two ellipses in the same figure
%                x(t) = 3 + 6cos(t), y(t) = -2 + 9sin(t)
% and
%                x(t) = 7 + 2cos(t), y(t) = 8 + 6sin(t.)
% There are several commands to enhance the readability of the graph.
%First of all note that the equations are converted into parametric form.

t = 0:pi/100:2*pi;
x1 = 3 + 6*cos(t);
y1 = -2 + 9*sin(t);
x2 = 7 + 2*cos(t);
y2 = 8 + 6*sin(t);
h1 = plot(x1,y1,'r',x2,y2,'b');

% Plot colours: y=yellow, m = magenta, c=cyan, r=red, g=green,
% b=blue,w=white,k=black.

set(h1,'LineWidth',1.25)
% To set the thickness of the plotted curves to a width of our choice.

axis('square')
% To force the axes to have square dimensions or else circular curves may
% not necessarily look circular.

legend('ellipse1', 'ellipse2')
xlabel('x')

h = get(gca,'xlabel');
%gca= get current axis; the axis targetted here is x-axis.

set(h,'FontSize',12)
set(gca,'XTick',-4:10)
% Specify font size and tick marking along the current axis.

ylabel('y')

h = get(gca,'ylabel');
set(h,'FontSize',20)
set(gca,'YTick',-12:2:14)
title('Graphs of (x-3)^2/36+(y+2)^2/81 = 1 and (x-7)^2/4+(y-8)^2/36 = 1.')

h = get(gca,'Title');
set(h,'FontSize',12)
grid
