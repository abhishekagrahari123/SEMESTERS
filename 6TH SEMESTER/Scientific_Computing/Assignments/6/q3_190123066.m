clc;
clear;
f = @(x,y) (x*y-y^2)/(x^2);
act_val = @(x) x/(0.5 + log(x));
err = @(a,b) abs(a-b);
euler_method = @(x,y,h) y + h*f(x,y); 

y_euler=2;
y_rk2 = 2;
y_rk4 = 2;
h = 0.1;
fprintf('\t\t\t\t\t\t\t\t Table 1: With h = 0.1 \nx    \t    EM   \t    Error(EM)  \t\t   RK2   \t   Error(RK2)  \t      RK4    \t   Error(RK4)\n');
for x = 1:h:2
    if x == 1.2 || x== 1.4 || x == 1.6 || x == 1.8 || x== 2
        fprintf('%.1f  %.12f  %.12f  %.12f  %.12f  %.12f  %.12f\n', x, y_euler, err(y_euler, act_val(x)), y_rk2, err(y_rk2, act_val(x)), y_rk4, err(y_rk4, act_val(x)));
    end
    y_euler = euler_method(x,y_euler,h);
    
    k1_rk2 = h*f(x,y_rk2);
    k2_rk2 = h*f(x + h, y_rk2 + k1_rk2);
    y_rk2 = y_rk2 + (k1_rk2 + k2_rk2)/2;

    k1_rk4 = h*f(x,y_rk4);
    k2_rk4 = h*f(x + h/2, y_rk4 + k1_rk4/2);
    k3_rk4 = h*f(x + h/2 , y_rk4 + k2_rk4/2);
    k4_rk4 = h*f(x + h, y_rk4 + k3_rk4);
    y_rk4 = y_rk4 + (k1_rk4 + 2*k2_rk4 + 2*k3_rk4 + k4_rk4)/6; 
end

y_euler=2;
y_rk2 = 2;
y_rk4 = 2;
h = 0.01;
fprintf('\n\t\t\t\t\t\t\t\t Table 2: With h = 0.01 \nx    \t    EM   \t    Error(EM)  \t\t   RK2   \t   Error(RK2)  \t      RK4    \t   Error(RK4)\n');
for x = 1:h:2
    if x == 1.2 || x== 1.4 || x == 1.6 || x == 1.8 || x== 2
        fprintf('%.1f  %.12f  %.12f  %.12f  %.12f  %.12f  %.12f\n', x, y_euler, err(y_euler, act_val(x)), y_rk2, err(y_rk2, act_val(x)), y_rk4, err(y_rk4, act_val(x)));
    end

    y_euler = euler_method(x,y_euler,h);
    
    k1_rk2 = h*f(x,y_rk2);
    k2_rk2 = h*f(x + h, y_rk2 + k1_rk2);
    y_rk2 = y_rk2 + (k1_rk2 + k2_rk2)/2;

    k1_rk4 = h*f(x,y_rk4);
    k2_rk4 = h*f(x + h/2, y_rk4 + k1_rk4/2);
    k3_rk4 = h*f(x + h/2 , y_rk4 + k2_rk4/2);
    k4_rk4 = h*f(x + h, y_rk4 + k3_rk4);
    y_rk4 = y_rk4 + (k1_rk4 + 2*k2_rk4 + 2*k3_rk4 + k4_rk4)/6;
end
