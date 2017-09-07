% modinverse.m
% Finds the modular inverse of a mod m. (a_inv * a = 1 (mod m))

function ainv = modinverse(x, m)
    if gcd(x, m) ~= 1
        error('x has no inverse modulo m')
    end

    % d = ax + bm
    [d, a, b] = gcd(x, m);
    ainv = mod(a, m);
end
