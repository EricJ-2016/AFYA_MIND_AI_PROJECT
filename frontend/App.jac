cl { def App() -> any { return <div><h1>AFYA-MIND</h1></div>; } }
import {*} from react;

cl app {
    def App() {
        let [screen, setScreen] = useState("home");
        let [username] = useState("eric_demo");
        let [tool, setTool] = useState("PHQ9");
        let [answers, setAnswers] = useState(list.fill(0, 9));
        let [journal, setJournal] = useState("");
        let [result, setResult] = useState(null);

        def submit() {
            res = root spawn log_screening(
                username=username,
                tool=tool,
                answers=answers,
                journal=journal
            );
            setResult(res);
            setScreen("result");
        }

        def Home() = <div style={{"padding:"20px", fontFamily:"Arial"}>
            <h1>AFYA-MIND</h1>
            <p>Mental Health Screening & MentaBot Companion</p>
            <button onClick={setScreen("screening")}>Start Screening</button>
            <button onClick={async(){ 
                t = root spawn analyze_trends(username=username);
                alert("Most common trigger: " + t.most_common_trigger);
            }}>View My Trends</button>
        </div>;

        def Screening() = <div style={padding:"20px"}>
            <h2>{tool} Screening</h2>
            <select value={tool} onChange={setTool}>
                <option>PHQ9</option><option>GAD7</option><option>ARM16</option><option>WERCAP</option>
            </select><br/><br/>
            <textarea placeholder="How are you really feeling today?" value={journal} onChange={setJournal} rows=4 cols=40/><br/><br/>
            {answers.map((a,i)=><input key=i type="number" min=0 max=3 value=a onChange={v=> {
                na = answers.copy(); na[i]=int(v); setAnswers(na);
            }} /> )}
            <br/><br/>
            <button onClick={submit}>Get Results & Talk to MentaBot</button>
            <button onClick={setScreen("home")}>Back</button>
        </div>;

        def Result() = <div style={padding:"20px"}>
            <h2>Result: {result.result}</h2>
            <p>Score: {result.score} | Trigger detected: {result.trigger}</p>
            <h3>MentaBot says:</h3>
            <p style={whiteSpace:"pre-line"}>{result.suggestion}</p>
            <button onClick={setScreen("home")}>Done</button>
        </div>;

        if(screen=="home") return <Home/>;
        if(screen=="screening") return <Screening/>;
        return <Result/>;
    }
}
