clc;
clear all;
f = @(x) ((x-1.1)^2)*(x+1);
f_prime = @(x) ((x-1.1)^2) + 2*(x+1)*(x-1.1);
err = @(x) abs(1.1-x);
TOL = 10^(-5);
x = zeros(1,100);
xm = zeros(1,100);
t = 1;
tm = 1;
x(t) = 2;
xm(tm) = 2;

while abs(f(x(t))) >= TOL
    t = t + 1;
    x(t) = x(t-1) - f(x(t-1))/f_prime(x(t-1));
end

while abs(f(xm(tm))) >= TOL
    tm = tm + 1;
    xm(tm) = xm(tm-1) - 2*f(xm(tm-1))/f_prime(xm(tm-1));
end

fprintf('  Iteration     Newton Method           p\n')
for k = 1:t
    if k + 2 <= t
        fprintf('%8d %18.7f %18.7f\n',k,x(k), log10(err(x(k+2))/err(x(k+1))) /log10(err(x(k+1))/err(x(k))))
    else 
        fprintf('%8d %18.7f\n',k,x(k))
    end
end

fprintf('  Iteration  Modified Newton Method      p\n')
for k = 1:tm
    if k + 2 <= tm
        fprintf('%8d %18.7f %18.7f\n',k,xm(k), log10(err(xm(k+2))/err(xm(k+1))) /log10(err(xm(k+1))/err(xm(k))))
    else 
        fprintf('%8d %18.7f\n',k,xm(k))
    end
end


