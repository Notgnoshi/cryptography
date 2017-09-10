x = [1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0];
% The following sequence is from the textbook, page 47.
% x = [1 0 0 1 1 0 0 1 0 0 1 1 1 0 0 0 1 1 0 0 0 1 0 1 0 0 0 1 1 1 1 0 1 1 0 0 1 1 1 1 1 0 1 0 1 0 1 0 0 1 0 1 1 0 1 1 0 1 0 1 1 0 0 0 0 1 1 0 1 1 1 0 0 1 0 1 0 1 1 1 1 0 0 0 0 0 0 0 1 0 0 0 1 0 0 1 0 0 0 0];
% The following sequence is from the textbook, page 45.
% x = [0 1 1 0 1 0 1 1 1 1 0 0];
for size = 2:length(x)/2
    A = gen_matrix(x, size);
    d = mod(round(det(A)), 2);

    fprintf('size: %d det: %d (mod 2)\n', size, d);

    b = x(size + 1 : 2 * size);
    c = mod(A \ b', 2)';

    if isequal(x, recurrence(x, c, length(x) - size))
       fprintf('sequences equal\n');
       disp(A);
       disp(b);
       disp(c);
    end
end


function A = gen_matrix(seq, size)
    A = [];
    for i = 1:size
        A = [A; seq(i:i + size - 1)];
    end
end
