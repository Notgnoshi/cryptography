% modinverse.m
% Finds the modular inverse of a matrix A mod m.

function Ainv = modinverse(A, m)
    a = round(det(A));
    res = mod(a * 1:m, m);
    b = find(res == 1);
    Ainv = mod(b * round(a * inv(A)), m);
end
