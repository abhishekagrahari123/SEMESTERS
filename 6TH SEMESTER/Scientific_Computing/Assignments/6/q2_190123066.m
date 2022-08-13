clc;
clear;
W1 = 0.8535533903;
W2 = 0.1464466092;
f = @(x) x^3;
x1 = 0.5857864376;
x2 = 3.414213562;
integral_val = W1*f(x1)+W2*f(x2);
fprintf('Required value of the integral is %.15f\n', integral_val);