clc;
clear;
fun = @(x) exp((x.^2)./(-2));
err = @(a,b) abs(a-b);
for m = [1,2]
    fprintf("\nFor m = %d\n", m)
    fprintf(" N \t\t\t\t Srule \t\t\t\t\t Error \t\t\t\t\t Relative Error\n")
    a = -m;
    b = m;
    actual_prob = integral(fun, a, b)*(1/sqrt(2*pi));
    for N = [1, 50, 100, 200]
        h = (b-a)/N;
        Simpson_tot = 0;
        for i = 1:N
            a1 = a + (i-1)*h;
            a2 = a + i*h;
            Simpson_tot = Simpson_tot + simpson_rule(a1,a2);
        end
        Req_prob = Simpson_tot*(1/sqrt(2*pi));
        fprintf("%3.0f \t\t %.15f \t\t %.15f \t\t %.15f\n", N, Req_prob, err(actual_prob, Req_prob), err(actual_prob, Req_prob)/actual_prob);
    end

    fprintf("Actual Value of Required Probability : %.15f \n", actual_prob);
end

function val = f(x)
    val = exp((x^2)/(-2));
end

function val = simpson_rule(a,b)
    val = ((b-a)*(f(a) + 4*f((a + b)/2)+ f(b)))/6;
end