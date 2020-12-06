using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ControlPointGenerator : MonoBehaviour
{
    [SerializeField]
    private ArcMiddleCalculator _amc;

    /// <summary>
    /// Creates a list of control points based on the specified values
    /// </summary>
    /// <param name="segmentCount">the amount of corner points a course of the Track type should have.</param>
    /// <param name="minDist">the minimum distance a control point can have from the center.</param>
    /// <param name="maxDist">the maximum distance a control point can have from the center.</param>
    /// <param name="controlPointAbberation">the aberration of a control point position in degrees.</param>
    /// <returns></returns>
    public List<Vector2> GenerateControlPoints(int segmentCount, float minDist, float maxDist, float controlPointAbberation)
    {
        List<Vector2> controlPoints = new List<Vector2>(segmentCount);
        float segmentStep = 360 / (float)segmentCount;
        float step = 0;
        for (int i = 0; i < segmentCount; ++i)
        {
            float distance = Random.Range(minDist, maxDist);
            float angle = step + Random.Range(-(controlPointAbberation / 2), controlPointAbberation / 2);

            Vector2 position = new Vector2(
                Mathf.Cos(angle * Mathf.Deg2Rad),
                Mathf.Sin(angle * Mathf.Deg2Rad));

            controlPoints.Add(position * distance);
            step += segmentStep;
        }
        return controlPoints;
    }

    public List<TrackParts> GenerateTrackParts(List<Vector2> controlPoints)
    {
        List<TrackParts> trackParts = new List<TrackParts>();

        List<Straight> straights = this.ShortenLines(controlPoints);
        List<Arc> arcs = this.FindArcs(straights);

        for (int i = 0; i < straights.Count; i++)
        {
            trackParts.Add(straights[i]);
            trackParts.Add(arcs[i]);
        }

        return trackParts;
    }

    /// <summary>
    /// Step one for generating a track: Shorten all straights leading into corners.
    /// This returns a list of straights. Between those straights there is emptiness which needs to be filled
    /// up with arcs later
    /// </summary>
    /// <param name="controlPoints"></param>
    /// <returns></returns>
    private List<Straight> ShortenLines(List<Vector2> controlPoints)
    {
        List<Straight> straights = new List<Straight>();

        Vector2 p1 = controlPoints[0];
        Vector2 p2 = controlPoints[1];
        Vector2 p3 = controlPoints[2];

        Vector2 l1_p1, l1_p2, l2_p1, l2_p2;
        _amc.ShortenLines(p1, p2, p3, out l1_p1, out l1_p2, out l2_p1, out l2_p2);
        straights.Add(new Straight(l1_p1, l1_p2));
        straights.Add(new Straight(l2_p1, l2_p2));

        for (int i = 1; i < controlPoints.Count; i++)
        {
            p1 = controlPoints[i];
            p2 = controlPoints[(i + 1) % controlPoints.Count];
            p3 = controlPoints[(i + 2) % controlPoints.Count];

            _amc.ShortenLines(p1, p2, p3, out l1_p1, out l1_p2, out l2_p1, out l2_p2);

            straights[i].End = l1_p2;

            if (i == controlPoints.Count - 1)
            {
                //straights[i].Start = l1_p1;
                straights[0].Start = l2_p1;
            }
            else
                straights.Add(new Straight(l2_p1, l2_p2));
        }

        return straights;
    }

    private List<Arc> FindArcs(List<Straight> straights)
    {
        List<Arc> arcs = new List<Arc>();

        for(int i = 0; i < straights.Count; i++)
        {
            Straight sA = straights[i];
            Straight sB = straights[(i + 1) % straights.Count];

            Vector2 arcMiddle = _amc.GetArcMiddle2(sA.Start, sA.End, sB.Start, sB.End, out float angleTheta);
            float radius = (sA.End - arcMiddle).magnitude;
            float length = angleTheta * radius;
            arcs.Add(new Arc(sA.End, sB.Start, angleTheta, length, arcMiddle));
        }

        return arcs;
    }
}
