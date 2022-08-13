clc;
clear;
x = zeros(1,9);
y = zeros(1,9);
h = zeros(8);
f = @(x) 1/(1 + x^2);
for i = 1:9
    x(i) = -5 + 10*(i-1)/8;
    y(i) = f(x(i));
    if i > 1
        h(i-1) = x(i) - x(i-1);
    end
end
b = zeros(1,8);
for i = 1:8
    b(i) = (6/h(i))*(y(i + 1)-y(i));
end
u = zeros(1,7);
v = zeros(1,7);
for i = 1:7
    u(i) = 2*(h(i) + h(i + 1));
    v(i) = b(i + 1) - b(i);
end
in = zeros(7);
for i = 1:7
    in(i,i) = u(i);
    if i < 7
        in(i,i+1) = h(i);
    end
    if i > 1
        in(i,i-1) = h(i-1);
    end
end
M = in\transpose(v);
m = zeros(9);
m(1) = 0;
m(9) = 0;
m(2:8) = M;
N = 100;
xp = zeros(8,N);
yp = zeros(8,N);

for i = 1:8
    xp(i,:) = linspace(x(i),x(i + 1),N);
    for j = 1:100
        yp(i,j) = spine_interpolation(xp(i,j), m(i), m(i + 1), x(i), x(i+1), y(i), y(i + 1));
    end
    plot(xp(i,:),yp(i,:),'b');
    hold on;
end

x_actual = linspace(-5,5,300);
y_actual = 1./(1 + x_actual.^2);
plot(x_actual,y_actual);
hold on;
legend('Natural Cubic spline','','','','','','','','Actual Function'); xlabel('x'), ylabel('Function value'), title('Runge Example'), grid on;
function val = spine_interpolation(x, m0, m1, x0, x1, y0, y1)
    h = x1-x0;
    val = ((x1-x)^3)*m0/(6*h) + ((x-x0)^3)*m1/(6*h) + (y1/h-m1*h/6)*(x-x0) + (y0/h-m0*h/6)*(x1-x);
end
