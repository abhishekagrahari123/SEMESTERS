frclc;
clear;

h = 0.1;
y_prev = 1;
x_prev = 0;
TOL = 0.0001;
fprintf('\t x \t\t   y(x)\n');
for i = 1:2
    x = x_prev + h;
    y0 = y_prev + h*f(x_prev, y_prev);
    while(1)
        y1 = y_prev + h/2*(f(x_prev, y_prev) + f(x, y0));
        if abs(y1 - y0)/abs(y1) < TOL
            break;
        end
        y0 = y1;
    end
    y_prev = y1;
    x_prev = x;
    fprintf('%f \t %f\n', x, y1)
end

function val = f(x, y)
    val = x-1/y;
end
