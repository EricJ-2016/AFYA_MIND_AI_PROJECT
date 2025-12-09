import {*} from react;

cl app {
    def App() {
        let [screen, setScreen] = useState("home");
        let [username] = useState("demo_user");

        def submit(tool) {
            res = root spawn log_screening(
                username=username, tool=tool,
                answers=[2,2,2,2,2,2,2,2,2], journal="Work stress"
            );
            st.write("Score:", res.score, "→", res.result);
            st.write("MentaBot:", res.suggestion);
        }

        return <div>
            <h1>AFYA-MIND</h1>
            <button onClick={submit("PHQ-9")}>Test PHQ-9</button>
            <button onClick={submit("GAD-7")}>Test GAD-7</button>
            <button onClick={submit("WERCAP")}>Test WERCAP</button>
        </div>;
    }
}
