RGB = imread("/home/carlos/Documents/HISPACOLD/Images/ThI_2.bmp");

I = mat2gray(RGB);
imshow(I);
colormap jet;

RGB(RGB > 31000) = 0;

I = mat2gray(RGB, [29900 31000]);
imshow(I);

binaryimage = imbinarize(I);

binaryimage = imdilate(binaryimage, [1 1 1; 1 1 1; 1 1 1]);

figure(1), imshow(binaryimage);

binaryimage = uint16(binaryimage);

[W, H] = size(binaryimage);

binaryimage = region_labeling(binaryimage, W, H);

numblobs = max(binaryimage, [], "all") - 1;

for k = 1:numblobs
    J = (binaryimage == k+1);
    [rows, colums] = find(J);
    row1 = min(rows);
    row2 = max(rows);
    col1 = min(colums);
    col2 = max(colums);

    blobs = (binaryimage(row1:row2, col1:col2) == (k+1));

    w = row2 - row1 +1;
    h = col2 - col1 +1;
    Area = sum(J(:) == 1);
    %Area = w*h;
if Area>2

    fprintf('Blob ');
    fprintf(string(k));
    fprintf(' had an area of ');
    fprintf(string(Area));
    fprintf(' pixels.\n');

    subplot(double(numblobs), 1, double(k));
    imshow(blobs);
    drawnow;
end
end

function I = region_labeling(I, W, H)
label = 2;
for u = 1:W
    for v = 1:H
        if I(u,v) == 1
            I = flood_fill(I, u, v, label, W, H);
            label = label+1;
        end
    end
end
end
function I = flood_fill(I, u, v, label, W, H)
if u>=1 && u<=W && v>+1 && v<=H && I(u,v) == 1
    I(u,v) = label;
    I = flood_fill(I, u+1, v, label, W, H);
    I = flood_fill(I, u, v+1, label, W, H);
    I = flood_fill(I, u, v-1, label, W, H);
    I = flood_fill(I, u-1, v, label, W, H);
    I = flood_fill(I, u+1, v+1, label, W, H);
    I = flood_fill(I, u-1, v+1, label, W, H);
    I = flood_fill(I, u+1, v-1, label, W, H);
    I = flood_fill(I, u-1, v-1, label, W, H);

end
end
