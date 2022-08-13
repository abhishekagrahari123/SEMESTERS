% we have to calculate g(1) which means integral 0 to 1 e^(-x^2)
clc;
clear;
a = 0;
b = 1;
actual_area = 0.74682413;
err = @(a,b) abs(a-b);

fprintf(" N \t\t\t\t Rrule \t\t\t\t Trule \t\t\t\t Srule " + ...
    "\t\t\t\t Er \t\t\t\t Et \t\t\t\t Es\n")
for N = [50, 100, 200]
    h = (b-a)/N;
    Rectangle_tot = 0;
    Trapezoidal_tot = 0;
    Simpson_tot = 0;
    for i = 1:N
        a1 = a + (i-1)*h;
        a2 = a + i*h;
        Rectangle_tot = Rectangle_tot + left_rectangle_rule(a1, a2);
        Trapezoidal_tot = Trapezoidal_tot + trapezoidal_rule(a1, a2);
        Simpson_tot = Simpson_tot + simpson_rule(a1,a2);
    end
    fprintf("%3.0f \t\t %.10f \t\t %.10f \t\t %.10f \t\t" + ...
        " %.10f \t\t %.10f \t\t %.10f\n", ...
        N, Rectangle_tot, Trapezoidal_tot, Simpson_tot, ...
        err(actual_area, Rectangle_tot), err(actual_area, Trapezoidal_tot), ...
        err(actual_area, Simpson_tot));
end

function val = f(x)
    val = exp(-(x^2));
end

function val = left_rectangle_rule(a,b)
    val = (b-a)*f(a);
end

function val = trapezoidal_rule(a,b)
    val = ((b-a)*(f(a) + f(b)))/2;
end

function val = simpson_rule(a,b)
    val = ((b-a)*(f(a) + 4*f((a + b)/2)+ f(b)))/6;
end