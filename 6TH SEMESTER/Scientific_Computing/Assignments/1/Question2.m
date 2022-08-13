clc;
clear all;
TOL = 10^(-3);
g = @(x) sqrt(x + 2);
f = @(x) x^(2)-x-2;
x = zeros(1,100);
k = 2;
x(k) = g(x(k-1));

while abs(x(k)-x(k-1))/abs(x(k)) >= TOL
    k = k + 1;
    x(k) = g(x(k-1));
end

fprintf('       Xn               f(Xn)           Error \n')
for i = 2:k
    fprintf('   %5.9f      %5.9f     %5.9f\n',x(i),f(x(i)),abs(x(i)-x(i-1))/abs(x(i)))
end   
