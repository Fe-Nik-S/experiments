
export const dayOfYear = date => Math.floor((date - new Date(date.getFullYear(), 0, 0)) / (1000 * 60 * 60 * 24));


export const getColonTimeFromDate = date => date.toTimeString().slice(0, 8);


export const getDaysDiffBetweenDates = (dateInitial, dateFinal) =>
    (dateFinal - dateInitial) / (1000 * 3600 * 24);


export const isBeforeDate = (dateA, dateB) => dateA < dateB;


export const isSameDate = (dateA, dateB) => dateA.toISOString() === dateB.toISOString();


export const tomorrow = () => {
    let t = new Date();
    t.setDate(t.getDate() + 1);
    return t.toISOString().split('T')[0];
};
