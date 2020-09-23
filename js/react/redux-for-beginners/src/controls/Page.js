
import React, { PropTypes, Component } from 'react';


export default class Page extends Component {
    onYearBtnClick(e) {
        //console.log(e.target.innerText);
        this.props.getPhotos(e.target.innerText);
    }
    render() {
        const { query, photos, fetching, error } = this.props;
        const QUERIES = ['Laptop', 'Animal', 'Flowers', 'Girls', 'Rocks', 'Wind']
        return <div className='ib page' >
            <p>
                { QUERIES.map((item,index) => <button className='btn' key={index} onClick={::this.onYearBtnClick}>{item}</button> )}
            </p>
            <h3>Query: {query}</h3>
            { error ? <p className='error'> Error appeared during request...</p> : ''}
            {
                fetching ?
                <p>Loading...</p>
                :
                photos.map((image_url, index) =>
                    <div key={index} className='photo'>
                        <p><img src={image_url} /></p>
                    </div>
                )
            }
        </div>
    }
}

Page.propTypes = {
    query: PropTypes.string.isRequired,
    photos: PropTypes.array.isRequired,
    getPhotos: PropTypes.func.isRequired
}
