using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UIManager : MonoBehaviour
{
    [SerializeField]
    private ArcMiddleCalculator _amc;

    [SerializeField]
    private ControlPointGenerator _cpg;

    [SerializeField]
    private GeometryDisplay _gd;

    [SerializeField]
    private int _calculatorVersion = 1;

    public void RecalculateArcMiddle()
    {
        _gd.Cleanup();

        Vector2 p1 = new Vector2(Random.Range(-10.0f, 10.0f), Random.Range(-10.0f, 10.0f));
        Vector2 p2 = new Vector2(Random.Range(-10.0f, 10.0f), Random.Range(-10.0f, 10.0f));
        Vector2 p3 = new Vector2(p2.x, p2.y);
        Vector2 p4 = new Vector2(Random.Range(-10.0f, 10.0f), Random.Range(-10.0f, 10.0f));

        if (_calculatorVersion == 0)
            _amc.GetArcMiddle(p1, p2, p3, p4);
        else if (_calculatorVersion == 1)
        {
            _amc.ShortenLines(p1, p2, p4, out Vector2 l1_p1, out Vector2 l1_p2, out Vector2 l2_p1, out Vector2 l2_p2);
            _amc.GetArcMiddle2(l1_p1, l1_p2, l2_p1, l2_p2, out float angleTheta);
        }
    }

    public void GenerateTrack()
    {
        _gd.Cleanup();
        List<Vector2> controlpoints = _cpg.GenerateControlPoints(11, 20, 60, 20);
        _gd.ShowTrackControlPoints(controlpoints);

        List<TrackParts> trackParts = _cpg.GenerateTrackParts(controlpoints);
        foreach (TrackParts tp in trackParts)
        {
            if (tp is Straight)
                _gd.ShowLine(tp.Start, tp.End, new Color(0.1f, 0.2f, 0.9f));
            else
            {
                Arc a = tp as Arc;
                _gd.ShowPoint(a.MiddlePoint, Color.red, "ArcMiddle", 3);
                _gd.ShowLine(tp.Start, tp.End, new Color(0.5f, 0.5f, 0.1f));
            }
        }
        _gd.ShowPoint(new Vector3(0, Camera.main.transform.position.y, 0), Color.red, "camera", 1);


        TrackExporter te = new TrackExporter();
        te.SimpleExport(trackParts, "E:\\Studium\\dev\\CARLA_0.9.10\\PythonAPI\\util\\opendrive\\unity.xodr");
    }
}
