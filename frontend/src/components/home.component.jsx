import React from 'react';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import {makeStyles} from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import Link from '@material-ui/core/Link';


const useStyles = makeStyles(theme => ({
    root: {
        marginTop: '100px',
    },
    heroContent: {
        backgroundColor: theme.palette.background.paper,
        padding: theme.spacing(8, 0, 6),
    },
    heroButtons: {
        marginTop: theme.spacing(4),
    },
}));

export default function HomeComponent(props) {
    const classes = useStyles();
    return (
        <div className={classes.root}>
            <CssBaseline/>
            <main>
                <div className={classes.heroContent}>
                    <Container maxWidth="sm">
                        <Typography component="h1" variant="h2" align="center" color="textPrimary" gutterBottom
                                    style={{marginBottom: '50px'}}>
                            welcome
                        </Typography>
                        <div className={classes.heroButtons}>
                            <Grid container spacing={2} justify="center">
                                <Grid item>
                                    <Button variant="contained" color="primary" onClick={()=>{props.history.push('/signup')}}>
                                        Signup
                                    </Button>
                                </Grid>
                                <Grid item>
                                    <Button variant="outlined" color="primary" onClick={()=>{props.history.push('/login')}}>
                                        Login
                                    </Button>
                                </Grid>
                            </Grid>
                        </div>
                    </Container>
                </div>

            </main>
        </div>
    );
}