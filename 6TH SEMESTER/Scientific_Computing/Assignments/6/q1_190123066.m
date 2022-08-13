clc;
clear;
f = @(x) sin(2*x+2)/(x + 1);

integral_val = 5/9*f(-sqrt(3/5)) + 8/9*f(0) + 5/9*f(sqrt(3/5));
fprintf('Required value of the integral is %.15f\n', integral_val);
