% recurrence.m
% Given a vector of recurrence coefficients and a vector of initial conditions,
% generate a sequence of bits.

function seq = recurrence(x, c, seq_length)
    narginchk(3, 3);
    if size(x, 2) < size(c, 2)
        error('x should have at least as many elements as c');
    end

    BASE = 2;
    n = size(c, 2);
    for i = 1:seq_length
        % The dot product mod BASE of c and a sliding slice of x
        x(i + n) = mod(dot(c, x(i : i + n - 1)), BASE);
    end

    seq = x;
end
