const express = require('express');
const path = require('path');
const { spawn } = require('child_process'); 

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/simulate', (req, res) => {
    const { homeTeam, awayTeam } = req.body;
    console.log("Received data for simulation:", homeTeam, awayTeam);

    const validateTeam = (team) => {
        for (const playerName in team) {
            const details = team[playerName];
            if (!details || typeof details !== 'object' || !details.season || !details.team) {
                return `Missing or incorrect data for player: ${playerName}`;
            }
        }
        return true;
    };

    const homeTeamValidation = validateTeam(homeTeam);
    if (homeTeamValidation !== true) {
        return res.status(400).json({ success: false, message: homeTeamValidation });
    }

    const awayTeamValidation = validateTeam(awayTeam);
    if (awayTeamValidation !== true) {
        return res.status(400).json({ success: false, message: awayTeamValidation });
    }

    const pythonProcess = spawn('python', ['src/simulate.py', JSON.stringify(homeTeam), JSON.stringify(awayTeam)]);

    let dataToSend = '';
    pythonProcess.stdout.on('data', (data) => {
        console.log('Pipe data from python script ...');
        console.log(data.toString());  // Log raw data
        dataToSend += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
        dataToSend += `Error in Python script: ${data}`;
    });

    pythonProcess.on('close', (code) => {
        try {
            const parsedData = JSON.parse(dataToSend);
            if (parsedData.success) {
                res.json({ success: true, message: "Simulation complete!", homeScore: parsedData.home_score, awayScore: parsedData.away_score });
            } else {
                res.status(500).json({ success: false, message: parsedData.message });
            }
        } catch (error) {
            console.error("Failiure:", error);
            res.status(500).json({ success: false, message: "Failed to handle results", errorDetail: error.toString() });
        }
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
