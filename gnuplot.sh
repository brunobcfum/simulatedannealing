#!/usr/bin/env gnuplot

set xlabel '# of iteractions' 
set y2label 'Distance' tc lt 2
set ylabel 'Temp' tc lt 1
set y2tics 10 nomirror tc lt 2
plot [x=0:700000] [y=0.5:1] 'data.csv' u 1:3 every 1000 with linespoints title 'Temperature decaying', 'data.csv' u 1:2 every 1000 with linespoints axis x1y2 title 'Total distance'
