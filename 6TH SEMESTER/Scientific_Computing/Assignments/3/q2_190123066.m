clc;
clear;

fprintf("\tn \t\t\t En\n");
N = 5;
En = zeros(1,N);
X_axis = zeros(1,N);
for t = 1:N
    n = 2^t;
    nodal_pts = linspace(-1, 1, n + 1);
    dd = divided_difference_calculator(nodal_pts,n);
    En(t) = En_calculator(dd,nodal_pts,n+1);
    fprintf('\t%d\t%.15f\n', n, En(t));
    X_axis(t) = n;
end 

figure;
plot(X_axis,En, 'Marker','square');
xlabel('n');
ylabel('En');
title('En vs n');
grid on;

function dd = divided_difference_calculator(nodal_pts,n)
    dd = zeros(n+1,n+1);
    for i = 1:n+1
        dd(i,1) = exp(nodal_pts(i));
    end
    for i = 2:n+1
        r = i-1;
        for c = 2:i
            dd(r,c) = (dd(r+1,c-1) - dd(r,c-1))/(nodal_pts(r+c-1)-nodal_pts(r));
            r = r - 1;
        end
    end
end

function En = En_calculator(dd, nodal_pts, n)
    x = linspace(-1,1,501);
    En = 0;
    for p = 1:501
        tk = x(p);
        val = 0;
        for i = 1:n
            term = 1;
            for j = 1:i-1
                term = term*(tk-nodal_pts(j));
            end
            val = val + term*dd(1,i);
        end
        En = max(En,abs(exp(tk) - val));
    end    
end