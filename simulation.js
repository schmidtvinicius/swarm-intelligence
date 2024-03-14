const { createCanvas, loadImage } = require('canvas');
const fs = require('fs');


function dist(x1, y1, x2, y2) {
    return Math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2);
}


let Scene = {
    w: 600, h: 600, swarm: [], iteration_num: 0,
    neighbours(x, interactionRadius) {
        let r = [];
        for (let p of this.swarm) {
            if (dist(p.pos.x, p.pos.y, x.x, x.y) <= interactionRadius) {
                r.push(p);
            }
        }
        return r;
    }
};


class Particle {
    constructor(name) {
        this.name = name;
        this.pos = { x: Math.random() * Scene.w, y: Math.random() * Scene.h };
        // this.dir = { x: Math.random() * 2 - 1, y: Math.random() * 2 - 1 };
        this.dir = { x: Math.cos(Math.random() * Math.PI * 2), y: Math.sin(Math.random() * Math.PI * 2)};
    }
    wrap() {
        if (this.pos.x < 0) this.pos.x += Scene.w;
        if (this.pos.y < 0) this.pos.y += Scene.h;
        if (this.pos.x > Scene.w) this.pos.x -= Scene.w;
        if (this.pos.y > Scene.h) this.pos.y -= Scene.h;
    }
    draw(ctx) {
        ctx.fillStyle = 'black';
        ctx.beginPath();
        ctx.fill();
        ctx.arc(this.pos.x, this.pos.y, 5, 0, Math.PI * 2);
    }
    step(cohesionFactor, separationFactor) {
        let N = Scene.neighbours(this.pos),
            avg_sin = 0, avg_cos = 0,
            avg_p = { x: 0, y: 0 },
            avg_d = { x: 0, y: 0 };
        for (let n of N) {
            avg_p.x += n.pos.x;
            avg_p.y += n.pos.y;
            if (n != this) {
                let away = { x: this.pos.x - n.pos.x, y: this.pos.y - n.pos.y };
                let magSq = away.x * away.x + away.y * away.y;
                away.x /= magSq * separationFactor;
                away.y /= magSq * separationFactor;
                avg_d.x += away.x;
                avg_d.y += away.y;
            }
            avg_sin += Math.sin(Math.atan2(n.dir.y, n.dir.x)) / N.length;
            avg_cos += Math.cos(Math.atan2(n.dir.y, n.dir.x)) / N.length;
        }
        avg_p.x /= N.length; avg_p.y /= N.length;
        avg_d.x /= N.length; avg_d.y /= N.length;
        let avg_angle = Math.atan2(avg_cos, avg_sin);
        avg_angle += Math.random() * 0.5 - 0.25;
        this.dir = { x: Math.cos(avg_angle), y: Math.sin(avg_angle) };
        let cohesion = { x: avg_p.x - this.pos.x, y: avg_p.y - this.pos.y };
        cohesion.x /= cohesionFactor; cohesion.y /= cohesionFactor;
        this.dir.x += cohesion.x;
        this.dir.y += cohesion.y;
        avg_d.x *= 20; avg_d.y *= 20;
        this.dir.x += avg_d.x;
        this.dir.y += avg_d.y;
        this.dir.x *= 4;
        this.dir.y *= 4;
        this.pos.x += this.dir.x;
        this.pos.y += this.dir.y;
        this.wrap();
    }
}


function console_log_row(table, x, y, iteration, point) {
    table.push([point, x, y, iteration]);
    return table;
}


async function simulate(cohesionFactor, separationFactor) {
    const canvas = createCanvas(Scene.w, Scene.h);
    const ctx = canvas.getContext('2d');
    
    let table = [['id', 'x', 'y', 'iteration']];
    let i = 0;
    for (let _ of Array(200)) {
        Scene.swarm.push(new Particle(i));
        i++;
    }

    while (Scene.iteration_num <= 300) {
        ctx.clearRect(0, 0, Scene.w, Scene.h);
        for (let p of Scene.swarm) {
            p.step(cohesionFactor, separationFactor);
            p.draw(ctx);
            console_log_row(table, p.pos.x, p.pos.y, Scene.iteration_num, p.name);
        }
        Scene.iteration_num++;
    }

    const csv = table.map(row => row.join(',')).join('\n');
    fs.writeFileSync('./exercise_1.csv', csv);
    console.log('exercise_1.csv saved');
}

let foundOptimalParameters = false
const populationSize = 20
const boidsPerPopulation = 15
const steps = 300
const velocity = 4
const interactionRadius = 100
let cohesionFactor

while(!foundOptimalParameters){
    
}
