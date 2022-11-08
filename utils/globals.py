import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

development_mode: bool = True

PATH = os.getenv("APPDATA") + "\\TrustLock" if not development_mode else os.getcwd()

VERSION = "1.0.0"

DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE'], 'Desktop'))

DB_PATH = PATH + "\\database\\" if not development_mode else f"{os.getcwd()}/database/"
DB_NAME = "test.db" if development_mode else "trustlock.db"
DB_COPY_NAME = "copy.db"
KEY_FILE_NAME = "test.pkl" if development_mode else "trustlock.pkl"

FONT_NAME = "Roboto Condensed"
PICKLE_ENC: str = 'SqQ1-jsiAXjOmRWQqLWoMyzTWgW_Kxy8rc5aGKLG91k='

class CHAR_GROUPS:
    NUMBERS = [*range(48,58)]
    UPPERCASE = [*range(65, 91)]
    LOWERCASE = [*range(97, 123)]
    MATH = [37, 42, 43, 45, 47, 61, 94]
    PUNCTUATION = [33, 34, 39, 44, 46, 58, 59, 63, 96]
    SPECIAL = [35, 36, 64, 95, 124, 126]
    BRACKETS = [40, 41, 60, 62, 91, 93, 123, 125]


WORDS = [
    'blind', 'medium', 'aware', 'crosswalk', 'craft', 'draw', 'disappoint', 'understanding', 'concept', 'disagree',
    'bargain', 'doubt', 'routine', 'commission', 'slice', 'praise', 'thick', 'smoke', 'mirror', 'efflux', 'applaud',
    'delay', 'infrastructure', 'finance', 'fashionable', 'pawn', 'school', 'pool', 'pound', 'recession', 'bike', 'depend',
    'he', 'building', 'advantage', 'mark', 'crude', 'service', 'hay', 'satisfaction', 'stop', 'commemorate', 'guide', 'fool',
    'threaten', 'doctor', 'clarify', 'indication', 'scenario', 'corruption', 'sister', 'liability', 'withdraw', 'defendant',
    'administration', 'illness', 'win', 'positive', 'minority', 'so', 'bare', 'mind', 'us', 'literature', 'nominate', 'major',
    'settle', 'fruit', 'practical', 'automatic', 'opposed', 'sock', 'fix', 'hostile', 'do', 'half', 'examination', 'cabin',
    'like', 'turkey', 'fare', 'sticky', 'printer', 'resolution', 'abundant', 'feedback', 'incapable', 'decrease', 'unlawful',
    'disk', 'enhance', 'student', 'physics', 'van', 'deep', 'language', 'amputate', 'bell', 'incongruous', 'distinct', 'parking',
    'appear', 'deprive', 'feast', 'understand', 'temptation', 'rush', 'silence', 'neck', 'sun', 'miscarriage', 'exclude', 'course',
    'critic', 'hemisphere', 'minister', 'elephant', 'confidence', 'owe', 'discourage', 'performer', 'crystal', 'bite', 'sin',
    'majority', 'willpower', 'enter', 'collection', 'cold', 'elbow', 'aid', 'prevent', 'traction', 'still', 'restaurant',
    'loose', 'wheel', 'dine', 'concert', 'neglect', 'wood', 'dangerous', 'center', 'violation', 'charge', 'wild', 'communication',
    'cash', 'random', 'easy', 'bush', 'medal', 'gene', 'herb', 'brilliance', 'foster', 'responsibility', 'venture', 'analyst',
    'mutter', 'horseshoe', 'swim', 'small', 'fresh', 'beam', 'image', 'bake', 'real', 'recruit', 'departure', 'tray', 'outlet',
    'cave', 'grandfather', 'temporary', 'quaint', 'laborer', 'moving', 'battlefield', 'threshold', 'expectation', 'ethnic', 'poem',
    'layout', 'active', 'sleeve', 'dedicate', 'comprehensive', 'please', 'heart', 'mist', 'identification', 'cake', 'origin', 'face',
    'document', 'sensation', 'fold', 'gradual', 'storage', 'village', 'breed', 'circle', 'digress', 'legislature', 'chip', 'lighter',
    'hypothesis', 'joint', 'yearn', 'height', 'response', 'dorm', 'strong', 'leash', 'apology', 'nest', 'computing', 'shock', 'buttocks',
    'highway', 'oak', 'hall', 'campaign', 'organisation', 'headquarters', 'assumption', 'costume', 'rebellion', 'bowel', 'piece',
    'champion', 'plaster', 'heat', 'general', 'an', 'serious', 'resist', 'plead', 'pig', 'top', 'consumption', 'lawyer', 'soul', 'horizon',
    'relative', 'avenue', 'echo', 'slump', 'bother', 'shelf', 'impact', 'appendix', 'disability', 'breeze', 'rock', 'fabricate',
    'coalition', 'discount', 'undertake', 'promise', 'base', 'user', 'myth', 'text', 'pole', 'outside', 'business', 'mouse', 'handicap',
    'inflate', 'thoughtful', 'dog', 'dignity', 'publish', 'floor', 'pleasure', 'unfair', 'generation', 'second', 'aloof', 'blast',
    'portion', 'superior', 'harmony', 'exact', 'give', 'native', 'taste', 'freedom', 'recording', 'disorder', 'career', 'serve',
    'flock', 'battle', 'summary', 'banana', 'demonstration', 'favour', 'option', 'beat', 'confront', 'mean', 'title', 'affect',
    'baseball', 'econobox', 'wander', 'cope', 'perform', 'fortune', 'speech', 'trait', 'shrink', 'eliminate', 'salvation', 'cable',
    'grateful', 'grow', 'forum', 'revive', 'advertise', 'camera', 'is', 'open', 'prisoner', 'correspond', 'bag', 'adventure', 'approve',
    'paint', 'barrier', 'influence', 'capture', 'thaw', 'detective', 'hardship', 'diplomat', 'ear', 'public', 'ideal', 'demonstrate',
    'strategic', 'equinox', 'lily', 'curve', 'penny', 'ambition', 'equation', 'lend', 'speaker', 'feature', 'behave', 'few',
    'atmosphere', 'texture', 'achieve', 'kit', 'mistreat', 'thirsty', 'soprano', 'orbit', 'regard', 'mine', 'landscape', 'ward', 'full',
    'punch', 'assume', 'flower', 'siege', 'border', 'experiment', 'ignorant', 'hostage', 'aisle', 'choke', 'skate', 'drown', 'grand',
    'complete', 'heaven', 'abstract', 'intensify', 'garlic', 'relation', 'opposite', 'vain', 'disappear', 'function', 'generate',
    'contraction', 'assessment', 'negotiation', 'depression', 'telephone', 'dismiss', 'sacred', 'seasonal', 'partnership', 'of',
    'immune', 'soft', 'abandon', 'dramatic', 'mask', 'gown', 'citizen', 'category', 'descent', 'ladder', 'smart', 'agreement',
    'plagiarize', 'dull', 'request', 'absent', 'revise', 'eternal', 'industry', 'solve', 'broccoli', 'allocation', 'projection',
    'balance', 'multiply', 'situation', 'onion', 'debate', 'shoulder', 'overview', 'pity', 'prince', 'tycoon', 'unlikely', 'grass',
    'vegetable', 'torch', 'addition', 'adjust', 'passage', 'marriage', 'narrow', 'facility', 'gossip', 'direction', 'loot', 'restrain',
    'self', 'moment', 'complication', 'brother', 'wear', 'urge', 'argument', 'reputation', 'laser', 'bench', 'rhetoric', 'bland',
    'finished', 'retain', 'reaction', 'poll', 'genetic', 'smell', 'mile', 'house', 'stroke', 'recover', 'amuse', 'president',
    'stool', 'broadcast', 'matrix', 'contempt', 'insist', 'astonishing', 'countryside', 'packet', 'cheese', 'noble', 'momentum',
    'folklore', 'inspector', 'highlight', 'frog', 'sand', 'wind', 'black', 'critical', 'bathtub', 'stage', 'athlete', 'admit',
    'charity', 'cow', 'ground', 'allow', 'reproduce', 'hill', 'tread', 'copy', 'conceive', 'frozen', 'auditor', 'sofa', 'painter',
    'arrest', 'toss', 'rain', 'cassette', 'save', 'classify', 'scratch', 'high', 'spontaneous', 'update', 'trust', 'map', 'creed',
    'bless', 'folk', 'bloodshed', 'fascinate', 'witch', 'impulse', 'opponent', 'just', 'exempt', 'filter', 'difficulty', 'contrary',
    'software', 'flex', 'photograph', 'democratic', 'linear', 'interference', 'strain', 'admission', 'total', 'inch', 'inspire',
    'difficult', 'mosque', 'gallery', 'judicial', 'good', 'bury', 'direct', 'retirement', 'domination', 'competence', 'patience',
    'guideline', 'cute', 'cross', 'stain', 'disclose', 'finger', 'insert', 'continuation', 'heel', 'social', 'diamond', 'institution',
    'favorable', 'architecture', 'mug', 'density', 'sex', 'prove', 'despise', 'conglomerate', 'sink', 'reveal', 'terms', 'gold',
    'limited', 'weak', 'breast', 'export', 'scale', 'profession', 'restrict', 'maid', 'extract', 'carve', 'state', 'strike', 'eagle',
    'sandwich', 'quality', 'cord', 'contribution', 'mathematics', 'incredible', 'jungle', 'scramble', 'constant', 'file', 'behead',
    'pat', 'temple', 'fair', 'peak', 'grounds', 'cast', 'inspiration', 'bank', 'rub', 'pick', 'bed', 'match', 'timber', 'choose',
    'shadow', 'enlarge', 'east', 'staff', 'cat', 'priority', 'distributor', 'swipe', 'treasurer', 'instrument', 'fisherman', 'magnitude',
    'teacher', 'present', 'electron', 'fibre', 'impound', 'choice', 'tick', 'treatment', 'conclusion', 'compensation', 'sermon',
    'neutral', 'loyalty', 'pattern', 'norm', 'plug', 'craftsman', 'grace', 'horn', 'decay', 'plot', 'cathedral', 'rank', 'innovation',
    'precedent', 'truck', 'trick', 'oral', 'respect', 'spectrum', 'complain', 'meet', 'length', 'census', 'concern', 'reign', 'trance',
    'vote', 'think', 'cream', 'compound', 'deport', 'exposure', 'continental', 'attraction', 'help', 'permission', 'loss', 'authorise',
    'dilute', 'weigh', 'articulate', 'sensitive', 'perception', 'tile', 'risk', 'extend', 'arrangement', 'obese', 'drop', 'doll',
    'ignore', 'tiptoe', 'elect', 'no', 'rifle', 'shiver', 'stem', 'bomb', 'tropical', 'day', 'consciousness', 'confine', 'constraint',
    'book', 'trunk', 'elapse', 'fitness', 'replace', 'hand', 'work', 'church', 'wisecrack', 'sickness', 'reservoir', 'migration',
    'exile', 'disaster', 'quotation', 'concede', 'abolish', 'pump', 'quest', 'dairy', 'consolidate', 'carrot', 'tire', 'convenience',
    'belly', 'creep', 'incentive', 'correction', 'ghostwriter', 'admiration', 'accountant', 'crossing', 'slot', 'use', 'stream',
    'welcome', 'royalty', 'widen', 'offensive', 'offspring', 'catch', 'discuss', 'entertain', 'eject', 'system', 'memory', 'lesson',
    'slap', 'air', 'proof', 'courage', 'assertive', 'occupation', 'looting', 'bridge', 'decoration', 'triangle', 'lock', 'chimpanzee',
    'murder', 'water', 'expression', 'velvet', 'chance', 'great', 'gutter', 'favourite', 'diet', 'adopt', 'conservation', 'sleep',
    'rough', 'preference', 'skin', 'me', 'rhythm', 'pit', 'commitment', 'presidential', 'forward', 'conversation', 'blade', 'landowner',
    'captain', 'frank', 'dynamic', 'shoot', 'memorial', 'up', 'dialogue', 'humanity', 'potential', 'hour', 'medicine', 'describe',
    'important', 'first', 'ton', 'rent', 'swell', 'fear', 'gas', 'sector', 'lie', 'interrupt', 'winner', 'wedding', 'roll', 'parallel',
    'coat', 'prison', 'width', 'Sunday', 'pioneer', 'original', 'stall', 'suspicion', 'cool', 'child', 'broken', 'distortion',
    'visible', 'guest', 'reinforce', 'dip', 'computer', 'forbid', 'chemistry', 'effective', 'satellite', 'investment', 'rotation',
    'proud', 'charter', 'other', 'sensitivity', 'short', 'biology', 'bill', 'standard', 'combine', 'dividend', 'heal', 'feminist',
    'pace', 'counter', 'century', 'constitutional', 'quarrel', 'winter', 'colon', 'integration', 'ask', 'suggest', 'team', 'presidency',
    'skeleton', 'scheme', 'cutting', 'large', 'will', 'decorative', 'rotate', 'wonder', 'eaux', 'joystick', 'zero', 'fame',
    'waist', 'sodium', 'tight', 'attractive', 'closed', 'overlook', 'celebration', 'formula', 'referral', 'blackmail', 'affair', 'nap',
    'suspect', 'lost', 'appeal', 'arrange', 'distort', 'hope', 'ethics', 'view', 'entitlement', 'quantity', 'trap', 'instinct', 'beginning',
    'bounce', 'yard', 'cousin', 'beer', 'colony', 'date', 'ticket', 'bottle', 'clock', 'salad', 'evoke', 'secular', 'trustee', 'basket',
    'angel', 'writer', 'rage', 'feather', 'reserve', 'visual', 'definite', 'long', 'ring', 'tree', 'ministry', 'professional', 'forestry',
    'coffin', 'appetite', 'tablet', 'colleague', 'buffet', 'ordinary', 'emotion', 'father', 'infection', 'symbol', 'south', 'curl',
    'combination', 'architect', 'gap', 'sphere', 'improve', 'isolation', 'profit', 'kneel', 'mystery', 'network', 'resource', 'tender',
    'example', 'stay', 'wording', 'mass', 'jaw', 'register', 'string', 'button', 'cluster', 'particle', 'background', 'transmission',
    'repeat', 'throw', 'favor', 'wrist', 'stretch', 'glacier', 'pause', 'ballet', 'lounge', 'novel', 'flag', 'definition', 'splurge',
    'union', 'sniff', 'performance', 'drug', 'brag', 'control', 'knowledge', 'applied', 'absorption', 'credit', 'tribute', 'exploit',
    'rob', 'honest', 'current', 'variation', 'season', 'headline', 'singer', 'constituency', 'revolutionary', 'hip', 'oil', 'bear',
    'cotton', 'warning'
    ]