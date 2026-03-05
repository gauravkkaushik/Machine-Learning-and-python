from src import utils

@utils.query
def acts(act_id=None):
    """
    Fetches all acts or a specific act by ID.
    """
    return f"""
    SELECT * FROM act 
    {f'WHERE act.id = {act_id}' if act_id else ''}
    """

@utils.query
def scenes(act_id=None, speaker=None):
    """
    Retrieves scenes, optionally filtered by act_id or a specific speaker's name.
    """
    q = f"""
    SELECT DISTINCT scene.*
    FROM scene
    """

    # If filtering by speaker, join through the speech and speaker tables
    if speaker:
        q += """
        INNER JOIN speech
            ON scene.id = speech.scene_id
        INNER JOIN speaker
            ON speech.speaker_id = speaker.id
        """
    
    # Dynamic WHERE clause construction
    if any([act_id, speaker]):
        q += f"""
        WHERE
        {f'scene.act_id = {act_id} {"AND" if speaker else ""}' if act_id else ''}
        {f'LOWER(speaker.text) = {speaker.lower()}' if speaker else ''}
        """
    
    q += 'ORDER BY scene.act_id, scene.id'

    return q



@utils.query
def speakers(scene=None, act=None, speaker_id=None):
    """
    Identifies speakers present in a specific scene, act, or by a specific ID.
    """
    q = f"""
        SELECT DISTINCT speaker.text speaker
                     , speaker.id
        FROM speaker
        INNER JOIN speech
            ON speaker.id = speech.speaker_id
        INNER JOIN scene
            ON speech.scene_id = scene.id
        """

    # Multi-condition filtering
    if any([scene, act, speaker_id]):
        q += f"""WHERE 
        {f"scene.id = {scene} {'AND' if act else ''}" if scene else ''}
        {f"scene.act_id = {act} {'AND' if speaker_id else ''}" if act else ''}
        {f"speaker.id = {speaker_id}" if speaker_id else ''}
        """

    return q

@utils.remove_stopwords    # Custom decorator to filter out common words (the, a, is)
@utils.remove_punctuation  # Custom decorator to strip punctuation from results
@utils.query
def word_count(speaker=None, act=None, scene=None):
    """
    Calculates frequency of words used by a specific speaker, 
    within a specific act or scene.
    """
    return f"""
    SELECT LOWER(word.text) "word"
         , COUNT(*) "word_count"
    FROM scene
    LEFT JOIN speech
        ON scene.id = speech.scene_id
    INNER JOIN speaker
        ON speech.speaker_id = speaker.id
    INNER JOIN line
        ON speech.id = line.speech_id
    INNER JOIN word
        ON line.id = word.line_id
    
    /* Dynamic filter block */
    {"WHERE" if any([speaker, act, scene]) else ""}
    {f"scene.act_id = {act} {'AND' if any([speaker, scene]) else ''}" if act else ""}
    {f"LOWER(speaker.text) = '{speaker.lower()}' {'AND' if scene else ''}" if speaker else ""}
    {f"scene.id = {scene}" if scene else ""}
    
    GROUP BY 1
    ORDER BY 2 asc
    """
    
