clc;
clear;

solve(-1, 0, 1);
fprintf('\n\n');
solve(0,-1,-10);

function solve(a1, a2, a3)
    fprintf('For a1 = %f, a2 = %f, a3 = %f\n', a1, a2, a3);
    fprintf('N    \t\t EM \t\t\t\t\t\t\t\t RK4 \t\t\t\t\t Error(EM)   \t\t\t\t Error(RK4)\n')
    for N = [10, 20, 40, 80]
        h = 1/N;
        A = 1/2*[a2+a3 a3-a1 a2-a1; a3-a2 a1+a3 a1-a2; a2-a3 a1-a3 a1+a2];
        y1 = [1;1;1];
        y2 = [1;1;1];
        for i = 1:N
            y1_prev = y1;
            y1 = y1_prev + h*f(A, y1_prev);
        end
        for i = 1:N
            y2_prev = y2;
            k1 = h*f(A, y2_prev);
            k2 = h*f(A, y2_prev + k1/2);
            k3 = h*f(A, y2_prev + k2/2);
            k4 = h*f(A, y2_prev + k3);
            y2 = y2_prev + 1/6*(k1 + 2*k2 + 2*k3 + k4);
        end
        act_val = act(a1,a2,a3);
        err1 = error(act_val, y1);
        err2 = error(act_val, y2);
        fprintf('%d  [%f %f %f] [%f %f %f] [%f %f %f] [%f %f %f] \n', N, y1(1), y1(2), y1(3), y2(1), y2(2),  y2(3), err1(1),err1(2),err1(3),err2(1),err2(2),err2(3) );
    end
end

function y_prime = f(A, y)
    y_prime = A*y;
end

function err = error(a, b)
    err = abs(a-b);
end

function val = act(a1, a2, a3)
    y1 = -exp(a1) + exp(a2) + exp(a3);
    y2 = exp(a1) - exp(a2) + exp(a3);
    y3 = exp(a1) + exp(a2) - exp(a3);
    val = [y1; y2; y3];
end