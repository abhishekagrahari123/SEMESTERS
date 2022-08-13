clc;
clear;
h = 0.001;
x0 = 0.4;
fp_actual = 1.081072;
diff1 = @(x,h) (f(x + h) - f(x-h))/(2*h);
diff2 = @(x,h) (-f(x + 2*h) + 8*f(x + h)-8*f(x-h) + f(x-2*h))/(12*h);
err_calc = @(a,b) abs(a-b);

d1 = diff1(x0,h);
d2 = diff2(x0,h);
fprintf("Using Central difference f_prime = %.15f and Error = %.15f\n", d1, err_calc(d1, fp_actual));
fprintf("Using Given formula f_prime = %.15f and Error = %.15f\n", d2, err_calc(d2, fp_actual));

function val = f(x)
    X = [0.398, 0.399, 0.400, 0.401, 0.402];
    Fx = [0.408591, 0.409671, 0.410752, 0.411834, 0.412915];
    val = 0;
    for i = 1:5
        if x == X(i)
            val = Fx(i);
        end
    end
end
