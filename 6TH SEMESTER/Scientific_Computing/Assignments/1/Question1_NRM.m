clc;
clear all;
f = @(x) exp(-x)-sin(x);
f_prime = @(x) -exp(-x)-cos(x);
TOL = 10^(-5);
x = zeros(1,100);
t = 1;
x(t) = pi/4;

while abs(f(x(t))) >= TOL
    t = t + 1;
    x(t) = x(t-1) - f(x(t-1))/f_prime(x(t-1));
end

fprintf('  Iteration   Newton Raphson Method\n')
for k = 1:t
    fprintf('   %5d          %8.8f\n',k,x(k))
end   
