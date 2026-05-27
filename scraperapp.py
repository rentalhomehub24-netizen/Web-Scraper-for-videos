from flask import Flask, render_template_string, request, jsonify
import difflib
import time

app = Flask(__name__)

# Mock Database: Aap jo naam dhoondna chahte hain
ANIME_DATABASE = [
    "Solo Leveling Season 1",
    "Solo Leveling Season 2",
    "Solo Leveling Season 3",
    "Naruto Shippuden",
    "One Piece",
    "Attack on Titan"
]

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/check-name', methods=['POST'])
def check_name():
    data = request.json
    user_query = data.get('query', '')
    matches = difflib.get_close_matches(user_query.title(), ANIME_DATABASE, n=1, cutoff=0.3)
    if matches:
        return jsonify({"status": "suggest", "matched_name": matches[0]})
    return jsonify({"status": "not_found", "message": "No match found. Try another name."})

@app.route('/fetch-links', methods=['POST'])
def fetch_links():
    data = request.json
    confirmed_name = data.get('confirmed_name', '')
    time.sleep(2) # Loading effect
    
    # Note: Solo Leveling Season 3 abhi production mein hai (2026), isliye iska content officially nahi aaya.
    if "Season 3" in confirmed_name:
        return jsonify({
            "status": "success",
            "links": [{"quality": "Official Trailer / Preview", "url": "https://youtube.com", "type": "Watch"}],
            "note": "Note: Solo Leveling Season 3 is currently in production. Displaying official updates."
        })
        
    links = [
        {"quality": "1080p Web-DL (Direct Link)", "url": "https://example.com", "type": "Download"},
        {"quality": "720p Bluray Torrent", "url": "magnet:?xt=urn:btih:123", "type": "Torrent"}
    ]
    return jsonify({"status": "success", "links": links})

# v0.dev dynamic design template with theme switch
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LinkStream AI</title>
    <script src="https://jsdelivr.net"></script>
    <style>body { transition: background-color 0.3s, color 0.3s; }</style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen font-sans">
    <header class="p-4 border-b border-slate-700/50 flex justify-between items-center bg-slate-950/40">
        <h1 class="text-xl font-bold tracking-wider text-indigo-400">⚡ LinkStream AI</h1>
        <button id="themeToggle" class="px-4 py-2 bg-slate-800 text-xs rounded-full border border-slate-700 hover:bg-slate-700 cursor-pointer">☀️ Light Mode</button>
    </header>
    <main class="max-w-2xl mx-auto mt-12 p-6">
        <div class="bg-slate-800/50 border border-slate-700/60 rounded-2xl p-6 shadow-xl backdrop-blur-md" id="mainCard">
            <label class="block text-sm font-medium mb-2 text-slate-400">Enter Anime/Series Name:</label>
            <div class="flex gap-2">
                <input type="text" id="searchInput" placeholder="e.g., solo lvl s3, sl s2" class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-indigo-500">
                <button id="searchBtn" class="bg-indigo-600 hover:bg-indigo-700 px-6 py-3 rounded-xl font-semibold cursor-pointer transition">Search</button>
            </div>
            <div id="suggestionBox" class="hidden mt-4 p-4 bg-indigo-950/50 border border-indigo-500/30 rounded-xl">
                <p class="text-sm">Did you mean: <span id="correctedName" class="font-bold text-indigo-400 text-lg"></span>?</p>
                <div class="mt-3 flex gap-2">
                    <button id="confirmYes" class="bg-emerald-600 hover:bg-emerald-700 px-4 py-1.5 rounded-lg text-xs font-bold cursor-pointer">Yes, Fetch Links</button>
                    <button id="confirmNo" class="bg-rose-600 hover:bg-rose-700 px-4 py-1.5 rounded-lg text-xs font-bold cursor-pointer">No, Cancel</button>
                </div>
            </div>
            <div id="loader" class="hidden mt-6 text-center py-6">
                <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-500 mx-auto"></div>
                <p class="text-xs text-slate-400 mt-3">Scanning public indexes and APIs for verified links...</p>
            </div>
            <div id="resultsBox" class="hidden mt-6 border-t border-slate-700/60 pt-4">
                <h3 class="text-sm font-semibold text-slate-400 mb-3">Verified Links Found:</h3>
                <div id="linksContainer" class="space-y-2"></div>
                <p id="systemNote" class="text-xs text-amber-400 mt-3 italic"></p>
            </div>
        </div>
    </main>
    <script>
        const themeToggle = document.getElementById('themeToggle');
        const searchInput = document.getElementById('searchInput');
        const searchBtn = document.getElementById('searchBtn');
        const suggestionBox = document.getElementById('suggestionBox');
        const correctedNameSpan = document.getElementById('correctedName');
        const confirmYes = document.getElementById('confirmYes');
        const confirmNo = document.getElementById('confirmNo');
        const loader = document.getElementById('loader');
        const resultsBox = document.getElementById('resultsBox');
        const linksContainer = document.getElementById('linksContainer');
        const systemNote = document.getElementById('systemNote');
        let targetName = "";

        themeToggle.addEventListener('click', () => {
            const html = document.documentElement;
            if (html.classList.contains('dark')) {
                html.classList.remove('dark');
                document.body.className = "bg-slate-100 text-slate-800 min-h-screen font-sans";
                document.getElementById('mainCard').className = "bg-white border border-slate-200 rounded-2xl p-6 shadow-xl";
                searchInput.className = "w-full bg-slate-50 border border-slate-300 rounded-xl px-4 py-3 text-slate-900 focus:outline-none focus:border-indigo-500";
                themeToggle.innerText = "🌙 Dark Mode";
            } else {
                html.classList.add('dark');
                document.body.className = "bg-slate-900 text-slate-100 min-h-screen font-sans";
                document.getElementById('mainCard').className = "bg-slate-800/50 border border-slate-700/60 rounded-2xl p-6 shadow-xl";
                searchInput.className = "w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-indigo-500";
                themeToggle.innerText = "☀️ Light Mode";
            }
        });

        async function checkName() {
            const query = searchInput.value.trim();
            if(!query) return;
            suggestionBox.classList.add('hidden');
            resultsBox.classList.add('hidden');
            const res = await fetch('/check-name', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ query: query })
            });
            const data = await res.json();
            if(data.status === 'suggest') {
                targetName = data.matched_name;
                correctedNameSpan.innerText = targetName;
                suggestionBox.classList.remove('hidden');
            } else { alert(data.message); }
        }
        searchBtn.addEventListener('click', checkName);
        confirmYes.addEventListener('click', async () => {
            suggestionBox.classList.add('hidden');
            loader.classList.remove('hidden');
            const res = await fetch('/fetch-links', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ confirmed_name: targetName })
            });
            const data = await res.json();
            loader.classList.add('hidden');
            linksContainer.innerHTML = '';
            systemNote.innerText = data.note || '';
            if(data.status === 'success') {
                data.links.forEach(link => {
                    const btn = document.createElement('a');
                    btn.href = link.url; btn.target = "_blank";
                    btn.className = "flex justify-between items-center p-3 bg-indigo-600/10 hover:bg-indigo-600/20 border border-indigo-500/30 rounded-xl text-sm font-medium";
                    btn.innerHTML = `<span>${link.quality}</span> <span class="bg-indigo-600 text-white px-3 py-1 rounded-lg text-xs">${link.type}</span>`;
                    linksContainer.appendChild(btn);
                });
                resultsBox.classList.remove('hidden');
            }
        });
        confirmNo.addEventListener('click', () => { suggestionBox.classList.add('hidden'); searchInput.value = ''; });
    </script>
</body>
</html>
"""
