clc;
clear;
n = 100;
x0 = linspace(-5,5,n);
y0 = zeros(1,n);
for i = 1:n
    y0(i) = interpolating_polynomial(x0(i));
end
y1 = 1./(1 + x0.^2);

plot(x0,y0);
xlabel('x');
ylabel('Function value');
title('Runge Example');
grid on;
hold on;

plot(x0, y1);
legend('Interpolating Polynomial', 'Actual function');
hold off;

function [val] = interpolating_polynomial(t) 
    f = @(x) 1/(1 + (x*x));    
    n = 9;
    x = linspace(-5,5,n);
    y = zeros(1,n);
    for i = 1:n
        y(i) = f(x(i));
    end
    val = 0.0;
    for i = 1:n
        sum = 1;
        for j = 1:n
            if j ~= i
                sum = sum * (t-x(j))/(x(i) - x(j)); 
            end
        end
        sum = sum * y(i);
        val = val + sum;
    end
end
