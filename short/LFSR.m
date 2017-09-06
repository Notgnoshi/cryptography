x = [1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1,1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0,0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1,1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0];
for size = 2:45
    A = gen_matrix(x, size);
    fprintf('size: %d det: %d\n', size, mod(round(det(A)), 26));
    if round(det(A)) ~= 0
        b = x(size + 1 : 2 * size);
        c = mod(A \ b', 2)';
        if isequal(x, recurrence(x, c, 90 - size))
           fprintf('sequences equal');
        end
    end
    
end


function A = gen_matrix(seq, size)
    A = [];
    for i = 1:size
        A = [A; seq(i:i + size - 1)];
    end
end
