clc;
clear all;
TOL = 10^(-5);
y = @(x) exp(-x) - sin(x);
a = 0;
b = pi/2;
c = b + (a - b)/2;
x = zeros(1,100);
i = 1;
x(i) = c;

while abs(y(c)) >= TOL
   if (y(a)*y(c)) < 0
       b = c;
   else 
       a = c;
   end
   c = b + (a - b)/2;
   i = i + 1;
   x(i) = c;
end

fprintf('  Iteration   Bisection Method\n')
for k = 1:i
    fprintf('   %5d          %8.7f\n',k,x(k))
end    
