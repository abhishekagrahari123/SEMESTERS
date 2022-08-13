clc;
clear;
syms x;
f = @(x) x*log(1 + x^2);
fpf = @(x,h) (f(x + h) - f(x))/h;
fpb = @(x,h) (f(x) - f(x-h))/h;
fpcd = @(x,h) (f(x + h) - f(x-h))/(2*h);
err_calc = @(a,b) abs(a-b);
x0 = 1;
fp_actual = eval((subs(diff(f,x,x0),x,x0)));
h = [0.1, 0.01, 0.001];
err = zeros(3);
fprime = zeros(3);
for i = 1:3
    f = fpf(x0,h(i));
    b = fpb(x0,h(i));
    cd = fpcd(x0,h(i));
    err(i,1) = err_calc(f, fp_actual);
    err(i,2) = err_calc(b, fp_actual);
    err(i,3) = err_calc(cd, fp_actual);
    fprime(i,1) = f;
    fprime(i,2) = b;
    fprime(i,3) = cd;
end

plot(h,err(:,1),"Marker","square");
hold on; 
xlabel('Step Size'); 
ylabel('Error');
title('Computational Error versus the Step Size');
grid on;
plot(h,err(:,2),"Marker","square");
hold on;
plot(h,err(:, 3),"Marker","square");
hold on;
legend('Forward', 'Backward', 'Central difference');
hold off;

fprintf("Estimated derivative value - \n");
fprintf(" h \t\t\t Forward \t\t\t Backward \t\t Central Difference\n");
for i = 1:3
    fprintf("%.3f \t %.15f \t %.15f \t %.15f\n", h(i), fprime(i,1), fprime(i,2), fprime(i,3));
end
fprintf("Error in Computation - \n");
fprintf(" h \t\t\t Forward \t\t\t Backward \t\t Central Difference\n");
for i = 1:3
    fprintf("%.3f \t %.15f \t %.15f \t %.15f\n", h(i), err(i,1), err(i,2), err(i,3));
end
