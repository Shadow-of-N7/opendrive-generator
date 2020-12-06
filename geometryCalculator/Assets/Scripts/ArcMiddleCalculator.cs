using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ArcMiddleCalculator : MonoBehaviour
{
    private void Start()
    {
        Vector2 p1 = new Vector2(10, 1);
        Vector2 p2 = new Vector2(13, 4);
        Vector2 p3 = new Vector2(13, 4);
        Vector2 p4 = new Vector2(17, 0);

        print("SignedAngle = " + Vector2.SignedAngle(p1 - p2, p3 - p4));
    }

    #region Versuch 1 mit Normalen

    public Vector2 GetArcMiddle(Vector2 p1, Vector2 p2, Vector2 p3, Vector2 p4)
    {
        Vector2 arcMiddle;

        float radius = this.GetRadius(p1, p2, p3, p4);
        Debug.Log("Radius: " + radius);

        bool middleFound = this.TryCalculateArcMiddleWithNormals(p1, p2, p3, p4, radius, 1, out arcMiddle);
        if (!middleFound)
            this.TryCalculateArcMiddleWithNormals(p1, p2, p3, p4, radius, -1, out arcMiddle);

        return arcMiddle;
    }

    private bool TryCalculateArcMiddleWithNormals(Vector2 p1, Vector2 p2, Vector2 p3, Vector2 p4, float radius, int normalDirection, out Vector2 arcMiddle)
    {
        arcMiddle = Vector2.zero;
        Color c = normalDirection == 1 ? new Color(0.8f, 0.1f, 0.1f) : new Color(0.5f, 0.05f, 0.05f);

        // --
        // Die Parallelen von A und B berechnen
        // --
        // Parallele von A:
        Vector2 parallelA1;
        Vector2 parallelA2;
        this.GetParallel(p1, p2, radius, normalDirection, out parallelA1, out parallelA2);

        // Parallele von B:
        Vector2 parallelB1;
        Vector2 parallelB2;
        this.GetParallel(p3, p4, radius, normalDirection, out parallelB1, out parallelB2);

        // --
        // Schnittpunkt der Parallelen berechnen
        // --
        bool isIntersecting = false;
        arcMiddle = GetIntersectionPointCoordinates(parallelA1, parallelA2, parallelB1, parallelB2, out isIntersecting);

        // Das liefert TRUE, wenn die Normale von A die Linie B echt schneidet. Dann muss A nämlich innerhalb sein.
        // Wenn die Normale außerhalb der beiden Vektoren ist, dann wird sie auch nicht mit B schneiden können.
        return this.DoVectorsIntersect(parallelA1, parallelA2, p3, p4);
    }

    private void GetParallel(Vector2 point1, Vector2 point2, float radius, int direction, out Vector2 parallelPoint1, out Vector2 parallelPoint2)
    {
        Vector2 perpA1 = this.RotateVector2(point2 - point1, Mathf.Deg2Rad * 90 * direction) + point1; // Vektor an Pivotpunkt p1 rotieren
        Vector2 perpA2 = this.RotateVector2(point1 - point2, Mathf.Deg2Rad * -90 * direction) + point2; // Vektor an Pivotpunkt p2 rotieren
        parallelPoint1 = Vector2.LerpUnclamped(point1, perpA1, radius / (point1 - perpA1).magnitude);
        parallelPoint2 = Vector2.LerpUnclamped(point2, perpA2, radius / (point2 - perpA2).magnitude);
    }

    private float GetRadius(Vector2 p1, Vector2 p2, Vector2 p3, Vector2 p4)
    {
        Vector2 A = p2 - p1;
        Vector2 B = p4 - p3;
        Vector2 shorterVector = A.magnitude > B.magnitude ? A : B;
        float shortRadius = shorterVector.magnitude * 0.35f;
        // Bei einem 90° Winkel wird ein Faktor der Länge des kürzeren Vektors als Radius verwendet
        if (Vector2.Angle(A, B) == 90)
        {
            return shortRadius;
        }
        else
        {
            Vector2 midA = Vector2.Lerp(p1, p2, 0.5f);
            Vector2 midB = Vector2.Lerp(p3, p4, 0.5f);

            float midDist = (midB - midA).magnitude;
            float radius = midDist * 0.35f;
            return shortRadius < radius ? shortRadius : radius;
        }
    }

    #endregion

    #region Versuch 2 mit Verkürzung

    /// <summary>
    /// Calculate two new shorter lines.
    /// Control points a, b and c are given. Both two lines start or end at point b
    /// Line 1: a -> b
    /// Line 2: b -> c
    /// </summary>
    public void ShortenLines(Vector2 a, Vector2 b, Vector2 c, out Vector2 l1_p1, out Vector2 l1_p2, out Vector2 l2_p1, out Vector2 l2_p2)
    {
        l1_p1 = Vector2.zero;
        l1_p2 = Vector2.zero;
        l2_p1 = Vector2.zero;
        l2_p2 = Vector2.zero;

        Vector2 line1 = b - a;
        Vector2 line2 = c - b;

        Vector2 shorterLine = line1.magnitude < line2.magnitude ? line1 : line2;
        float lengthToCut = shorterLine.magnitude * 0.3f;

        l1_p1 = a;
        l1_p2 = Vector2.LerpUnclamped(b, a, lengthToCut / (b - a).magnitude);
        l2_p1 = Vector2.LerpUnclamped(b, c, lengthToCut / (c - b).magnitude);
        l2_p2 = c;

        float mag1 = (b - l1_p2).magnitude;
        float mag2 = (b - l2_p1).magnitude;
        print("Dist 1: " + mag1);
        print("Dist 2: " + mag2);

        bool sameDist = Mathf.Abs(mag1 - mag2) < 0.1f ? true : false;
        if (sameDist)
            print("Success: Both lines were shortened the same amount");
        else
            Debug.LogWarning("ERROR: Line shortening isn't consistent");
    }


    /// <summary>
    /// Calculate the arc middle from two lines that aren't connected. They were shortened by the same amount before this operation.
    /// </summary>
    /// <param name="angleTheta">The inner angle of the arc</param>
    /// <returns></returns>
    public Vector2 GetArcMiddle2(Vector2 l1_p1, Vector2 l1_p2, Vector2 l2_p1, Vector2 l2_p2, out float angleTheta)
    {
        Vector2 arcMiddle = Vector2.zero;

        // --
        // An den Endpunkten eine Senkrechte aufstellen
        // --
        Vector2 perpl1 = this.RotateVector2(l1_p1 - l1_p2, Mathf.Deg2Rad * 90) + l1_p2; // Vektor an Pivotpunkt l1_p2 rotieren
        Vector2 perpl2 = this.RotateVector2(l2_p2 - l2_p1, Mathf.Deg2Rad * -90) + l2_p1; // Vektor an Pivotpunkt l2_p1 rotieren

        bool doIntersect = false;
        arcMiddle = this.GetIntersectionPointCoordinates(l1_p2, perpl1, l2_p1, perpl2, out doIntersect);
        print("Perpendicaluars intersect: " + doIntersect + " at " + arcMiddle);

        angleTheta = Vector2.SignedAngle(l1_p1 - l1_p2, l2_p1- l2_p2) * Mathf.Deg2Rad;

        return arcMiddle;
    }

    #endregion

    private Vector2 RotateVector2(Vector2 v, float degrees)
    {
        Vector2 result = new Vector2();
        result[0] = v.x * Mathf.Cos(degrees) - v.y * Mathf.Sin(degrees);
        result[1] = v.x * Mathf.Sin(degrees) - v.y * Mathf.Cos(degrees);
        return result;
    }

    /// <summary>
    /// Gets the coordinates of the intersection point of two lines.
    /// Quelle: https://blog.dakwamine.fr/?p=1943
    /// </summary>
    /// <param name="A1">A point on the first line.</param>
    /// <param name="A2">Another point on the first line.</param>
    /// <param name="B1">A point on the second line.</param>
    /// <param name="B2">Another point on the second line.</param>
    /// <param name="found">Is set to false of there are no solution. true otherwise.</param>
    /// <returns>The intersection point coordinates. Returns Vector2.zero if there is no solution.</returns>
    public Vector2 GetIntersectionPointCoordinates(Vector2 A1, Vector2 A2, Vector2 B1, Vector2 B2, out bool found)
    {
        float tmp = (B2.x - B1.x) * (A2.y - A1.y) - (B2.y - B1.y) * (A2.x - A1.x);

        if (tmp == 0)
        {
            // No solution!
            found = false;
            return Vector2.zero;
        }

        float mu = ((A1.x - B1.x) * (A2.y - A1.y) - (A1.y - B1.y) * (A2.x - A1.x)) / tmp;

        found = true;

        return new Vector2(
            B1.x + (B2.x - B1.x) * mu,
            B1.y + (B2.y - B1.y) * mu
        );
    }

    /// <summary>
    /// Nachschauen, ob sich zwei abgeschlossene Vektoren (Liniensegmente) schneiden
    /// Quelle: https://forum.unity.com/threads/line-intersection.17384/
    /// </summary>
    /// <param name="line1point1"></param>
    /// <param name="line1point2"></param>
    /// <param name="line2point1"></param>
    /// <param name="line2point2"></param>
    /// <returns></returns>
    private bool DoVectorsIntersect(Vector2 line1point1, Vector2 line1point2, Vector2 line2point1, Vector2 line2point2)
    {

        Vector2 a = line1point2 - line1point1;
        Vector2 b = line2point1 - line2point2;
        Vector2 c = line1point1 - line2point1;

        float alphaNumerator = b.y * c.x - b.x * c.y;
        float betaNumerator = a.x * c.y - a.y * c.x;
        float denominator = a.y * b.x - a.x * b.y;

        if (denominator == 0)
        {
            return false;
        }
        else if (denominator > 0)
        {
            if (alphaNumerator < 0 || alphaNumerator > denominator || betaNumerator < 0 || betaNumerator > denominator)
            {
                return false;
            }
        }
        else if (alphaNumerator > 0 || alphaNumerator < denominator || betaNumerator > 0 || betaNumerator < denominator)
        {
            return false;
        }
        return true;
    }
}
