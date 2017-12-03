from pytsp import atsp_tsp, run, dumps_matrix

matrix = [
    [ 0,    2903, 4695 ],
    [ 2903, 0,    5745 ],
    [ 4695, 5745, 0    ]]

matrix = np.array(matrix)

outf = "/tmp/myroute.tsp"
with open(outf, 'w') as dest:
    dest.write(dumps_matrix(matrix, name="My Route"))

tour = run(outf, start=10, solver="concorde")

print(tour['tour'])
print('solution', tour['solution'])