# Firefly Optimization
Sebagian besar spesies kunang-kunang mampu menghasilkan kilatan pendek. Diperkirakan bahwa fungsi utama dari kedipan adalah untuk menarik kunang-kunang dari lawan jenis dan mangsa potensial. Selain itu, sinyal flash dapat berkomunikasi dengan predator bahwa kunang-kunang memiliki rasa pahit.

## Model matematika
**Algoritma Firefly** didasarkan pada dua hal penting: perubahan intensitas cahaya dan daya tarik. Secara sederhana, diasumsikan bahwa daya tarik kunang-kunang didefinisikan oleh kecerahannya yang terhubung dengan fungsi obyektif.

Algoritma Firefly menggunakan model perilaku kunang-kunang sebagai berikut:

- Semua kunang-kunang mampu menarik satu sama lain terlepas dari gender mereka.
- Daya tarik kunang-kunang bagi individu lain sebanding dengan kecerahannya.
- Kunang-kunang yang kurang menarik bergerak ke arah yang paling menarik.
- Ketika jarak antara dua kunang-kunang meningkat, kecerahan yang terlihat dari kunang-kunang yang diberikan untuk yang lain menurun.
- Jika kunang-kunang tidak melihat kunang-kunang yang lebih terang dari dirinya sendiri, ia bergerak secara acak.

## Pseudocode
<pre>
Initialize the firefly population X=x<sub>1</sub>, x<sub>2</sub>, ... , x<sub>d</sub>;
&gamma; = 0.95;
FOR each firefly x<sub>i</sub> in the population DO
    I<sub>i</sub>=fitness(x<sub>i</sub>);
END

REPEAT
    FOR each firefly x<sub>i</sub> in the swarm DO
        FOR each other firefly x<sub>j</sub> in the swarm DO
            IF I<sub>j</sub> < I<sub>i</sub> THEN
                r<sub>ij</sub> = HammingDistance(x<sub>i</sub>, x<sub>j</sub>);
                n = Random(2, r<sub>ij</sub>&gamma;<sup>g</sup>);
                x<sub>i</sub> = InsertionFunction(x<sub>i</sub>,n);
            END
            Evaluate news solutions and update light intensity;
        END
    END
    Rank the fireflies and find the current best;
UNTIL termination criterion reached;
Rank the fireflies and return the best one;
</pre>