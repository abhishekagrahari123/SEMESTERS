clc;
clear;
a = 0;
b = 1;
actual_area = 0.0808308690;
err = @(a,b) abs(a-b);

fprintf(" N \t\t\t    Trapezoidal \t   Corrected Trapezoidal \t  Err_Trapezoidal \t Err_Corrected_Trapezoidal\n")
for N = [1, 50, 100, 200]
    h = (b-a)/N;
    Trapezoidal_tot = 0;
    Corr_Trapezoidal_tot = 0;
    for i = 1:N
        a1 = a + (i-1)*h;
        a2 = a + i*h;
        Trapezoidal_tot = Trapezoidal_tot + trapezoidal_rule(a1, a2);
        Corr_Trapezoidal_tot = Corr_Trapezoidal_tot + corrected_trapezoidal_rule(a1,a2);
    end
    fprintf("%3.0f \t\t %.15f \t\t %.15f \t\t %.15f \t\t %.15f\n", ...
        N, Trapezoidal_tot, Corr_Trapezoidal_tot, err(actual_area, Trapezoidal_tot), err(actual_area, Corr_Trapezoidal_tot));
end

function val = f(x)
    val = (x^2)*exp(-2*x);
end

function val = f_prime(x)
    val = 2*exp(-2*x)*(x-x^2);
end

function val = trapezoidal_rule(a,b)
    val = ((b-a)*(f(a) + f(b)))/2;
end

function val = corrected_trapezoidal_rule(a,b)
    val = trapezoidal_rule(a,b) + ((b-a)^2)*(f_prime(a)-f_prime(b))/12;
end