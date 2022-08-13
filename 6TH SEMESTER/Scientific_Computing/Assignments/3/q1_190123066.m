clc;
clear;
n = 50;
x0 = linspace(0,1,n);
y0 = zeros(1,n);
for i = 1:n
    y0(i) = interpolating_polynomial(x0(i));
end
x1 = 0:0.1:1;
y1 = [0.00000000000000, 0.11246291601828, 0.22270258921048, 0.32862675945913, 0.42839235504667, 0.52049987781305, 0.60385609084793, 0.67780119383742, 0.74210096470766, 0.79690821242283,0.84270079294971];

fprintf("\tx \t\t\t interpolating_pol(x)-table_data(x)\n");
for t= 1:11
    fprintf("%.10f \t\t %.10f\n",x1(t),interpolating_polynomial(x1(t))-y1(t))
end

plot(x0,y0);
xlabel('x');
ylabel('erf(x)');
title('Error Function Graph');
grid on;
hold on;

plot(x1,y1,'LineStyle','-', 'Marker','*');
legend('Interpolating Polynomial','Data in the table')
hold off;

function [val] = interpolating_polynomial(t) 
    x = [0, 0.5, 1.0];
    y_val = [0.00000000000000, 0.52049987781305, 0.84270079294971];
    L = @(x1,x2,x3) (((t-x2)*(t-x3))/((x1-x2)*(x1-x3)));
    val = y_val(1)*L(x(1),x(2),x(3)) + y_val(2)*L(x(2),x(1),x(3)) + y_val(3)*L(x(3),x(1),x(2));
end
